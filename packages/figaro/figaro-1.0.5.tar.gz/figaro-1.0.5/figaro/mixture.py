import numpy as np
import sys
import dill

from collections import Counter
from pathlib import Path

from scipy.special import gammaln, logsumexp
from scipy.stats import multivariate_normal as mn
from scipy.stats import invwishart, norm, invgamma

from figaro.decorators import *
from figaro.transform import *
from figaro.likelihood import evaluate_mixture_MC_draws, evaluate_mixture_MC_draws_1d, logsumexp_jit, log_norm
from figaro.exceptions import except_hook, FIGAROException
from figaro.utils import get_priors
from figaro.marginal import _condition, _marginalise

from numba import jit, njit, prange
from numba.extending import get_cython_function_address
import ctypes

#-----------#
# Utilities #
#-----------#

sys.excepthook = except_hook

"""
See https://stackoverflow.com/a/54855769
Wrapper (based on https://github.com/numba/numba/issues/3086) for scipy's cython implementation of gammaln.
"""

_PTR = ctypes.POINTER
_dble = ctypes.c_double
_ptr_dble = _PTR(_dble)

addr = get_cython_function_address("scipy.special.cython_special", "gammaln")
functype = ctypes.CFUNCTYPE(_dble, _dble)
gammaln_float64 = functype(addr)

#-----------#
# Functions #
#-----------#

@njit
def _numba_gammaln(x):
    return gammaln_float64(x)

@jit
def _student_t(df, t, mu, sigma, dim):
    """
    Multivariate student-t pdf.
    As in http://gregorygundersen.com/blog/2020/01/20/multivariate-t/
    
    Arguments:
        :float df:         degrees of freedom
        :float t:          variable (2d array)
        :np.ndarray mu:    mean (2d array)
        :np.ndarray sigma: variance
        :int dim:          number of dimensions
        
    Returns:
        :float: student_t(df).logpdf(t)
    """
    vals, vecs = np.linalg.eigh(sigma)
    logdet     = np.log(vals).sum()
    valsinv    = np.array([1./v for v in vals])
    U          = vecs * np.sqrt(valsinv)
    dev        = t - mu
    maha       = np.square(np.dot(dev, U)).sum(axis=-1)

    x = 0.5 * (df + dim)
    A = _numba_gammaln(x)
    B = _numba_gammaln(0.5 * df)
    C = dim/2. * np.log(df * np.pi)
    D = 0.5 * logdet
    E = -x * np.log1p((1./df) * maha)

    return (A - B - C - D + E)[0]

@jit
def update_alpha(alpha, n, K, burnin = 1000):
    """
    Update concentration parameter using a Metropolis-Hastings sampling scheme.
    
    Arguments:
        :double alpha: Initial value for concentration parameter
        :int n:        Number of samples
        :int K:        Number of active clusters
        :int burnin:   MH burnin
    
    Returns:
        :double: new concentration parameter value
    """
    a_old = alpha
    n_draws = burnin+np.random.randint(100)
    for i in prange(n_draws):
        a_new = a_old + (np.random.random() - 0.5)
        if a_new > 0.:
            logP_old = _numba_gammaln(a_old) - _numba_gammaln(a_old + n) + K * np.log(a_old) - 1./a_old
            logP_new = _numba_gammaln(a_new) - _numba_gammaln(a_new + n) + K * np.log(a_new) - 1./a_new
            if logP_new - logP_old > np.log(np.random.random()):
                a_old = a_new
    return a_old

@jit
def compute_t_pars(k, mu, nu, L, mean, S, N, dim):
    """
    Compute parameters for student-t distribution.
    
    Arguments:
        :double k:        Normal std parameter (for NIW)
        :np.ndarray mu:   Normal mean parameter (for NIW)
        :int nu:          Inverse-Wishart df parameter (for NIW)
        :np.ndarray L:    Inverse-Wishart scale matrix (for NIW)
        :np.ndarray mean: samples mean
        :np.ndarray S:    samples covariance
        :int N:           number of samples
        :int dim:         number of dimensions
    
    Returns:
        :int:        degrees of fredom for student-t
        :np.ndarray: scale matrix for student-t
        :np.ndarray: mean for student-t
    """
    # Update hyperparameters
    k_n, mu_n, nu_n, L_n = compute_hyperpars(k, mu, nu, L, mean, S, N)
    # Update t-parameters
    t_df    = nu_n - dim + 1
    t_shape = L_n*(k_n+1)/(k_n*t_df)
    return t_df, t_shape, mu_n

@jit
def compute_hyperpars(k, mu, nu, L, mean, S, N):
    """
    Update hyperparameters for Normal Inverse Gamma/Wishart (NIG/NIW).
    See https://www.cs.ubc.ca/~murphyk/Papers/bayesGauss.pdf
    
    Arguments:
        :double k:        Normal std parameter (for NIG/NIW)
        :np.ndarray mu:   Normal mean parameter (for NIG/NIW)
        :int nu:          Gamma df parameter (for NIG/NIW)
        :np.ndarray L:    Gamma scale matrix (for NIG/NIW)
        :np.ndarray mean: samples mean
        :np.ndarray S:    samples covariance
        :int N:           number of samples
    
    Returns:
        :double:     updated Normal std parameter (for NIG/NIW)
        :np.ndarray: updated Normal mean parameter (for NIG/NIW)
        :int:        updated Gamma df parameter (for NIG/NIW)
        :np.ndarray: updated Gamma scale matrix (for NIG/NIW)
    """
    k_n  = k + N
    mu_n = (mu*k + N*mean)/k_n
    nu_n = nu + N
    L_n  = L + S + k*N*((mean - mu).T@(mean - mu))/k_n
    return k_n, mu_n, nu_n, L_n

@jit
def compute_component_suffstats(x, mean, S, N, p_mu, p_k, p_nu, p_L):
    """
    Update mean, covariance, number of samples and maximum a posteriori for mean and covariance.
    
    Arguments:
        :np.ndarray x:    sample to add
        :np.ndarray mean: mean of samples already in the cluster
        :np.ndarray cov:  covariance of samples already in the cluster
        :int N:           number of samples already in the cluster
        :np.ndarray p_mu: NIG Normal mean parameter
        :double p_k:      NIG Normal std parameter
        :int p_nu:        NIG Gamma df parameter
        :np.ndarray p_L:  NIG Gamma scale matrix
    
    Returns:
        :np.ndarray: updated mean
        :np.ndarray: updated covariance
        :int N:      updated number of samples
        :np.ndarray: mean (maximum a posteriori)
        :np.ndarray: covariance (maximum a posteriori)
    """
    new_mean  = (mean*N+x)/(N+1)
    new_S     = (S + N*mean.T@mean + x.T@x) - new_mean.T@new_mean*(N+1)
    new_N     = N+1
    new_mu    = ((p_mu*p_k + new_N*new_mean)/(p_k + new_N))[0]
    new_sigma = (p_L + new_S + p_k*new_N*((new_mean - p_mu).T@(new_mean - p_mu))/(p_k + new_N))/(p_nu + new_N - x.shape[-1] - 1)
    
    return new_mean, new_S, new_N, new_mu, new_sigma

#-------------------#
# Auxiliary classes #
#-------------------#

class prior:
    """
    Class to store the NIW prior parameters
    See https://www.cs.ubc.ca/~murphyk/Papers/bayesGauss.pdf, sec. 9
    
    Arguments:
        :double k:        Normal std parameter
        :np.ndarray mu:   Normal mean parameter
        :int nu:          Wishart df parameter
        :np.ndarray L:    Wishart scale matrix
    
    Returns:
        :prior: instance of prior class
    """
    def __init__(self, k, L, nu, mu):
        self.k   = k
        self.nu  = np.max([nu, mu.shape[-1]+2])
        self.L   = L*(self.nu-mu.shape[-1]-1)
        self.mu  = mu

class component:
    """
    Class to store the relevant informations for each component in the mixture.
    
    Arguments:
        :np.ndarray x: sample added to the new component
        :prior prior:  instance of the prior class with NIG/NIW prior parameters
    
    Returns:
        :component: instance of component class
    """
    def __init__(self, x, prior):
        self.N     = 1
        self.mean  = x
        self.S     = np.identity(x.shape[-1])*0.
        self.mu    = np.atleast_2d((prior.mu*prior.k + self.N*self.mean)/(prior.k + self.N)).astype(np.float64)[0]
        self.sigma = np.identity(x.shape[-1]).astype(np.float64)*prior.L/(prior.nu - x.shape[-1] - 1)

class component_h:
    """
    Class to store the relevant informations for each component in the mixture.
    To be used in hierarchical inference.
    
    Arguments:
        :np.ndarray x:  event added to the new component
        :int dim:       number of dimensions
        :prior prior:   instance of the prior class with NIG/NIW prior parameters
        :double logL_D: logLikelihood denominator
    
    Returns:
        :component_h: instance of component_h class
    """
    def __init__(self, x, dim, prior, logL_D, mu_MC, sigma_MC, b_ones):
        self.dim    = dim
        self.N      = 1
        self.events = [x]
        self.means  = [x.means]
        self.covs   = [x.covs]
        self.log_w  = [x.log_w]
        self.logL_D = logL_D
        
        log_norm_D = logsumexp_jit(logL_D, b = b_ones)
        
        self.mu    = np.average(mu_MC, weights = np.exp(logL_D - log_norm_D), axis = 0)
        self.sigma = np.average(sigma_MC, weights = np.exp(logL_D - log_norm_D), axis = 0)
        if dim == 1:
            self.mu = np.atleast_2d(self.mu).T
            self.sigma = np.atleast_2d(self.sigma).T
            
class _density:
    """
    Class to initialise a common set of methods for mixture models. Not to be used
    """
    def __init__(self):
        pass
        
    def __call__(self, x):
        return self.pdf(x)

    def pdf(self, x):
        if self.n_cl == 0:
            raise FIGAROException("You are trying to evaluate an empty mixture.\n If you are using the density_from_samples() method, you may want to evaluate the output of that method.")
        if len(np.shape(x)) < 2:
            if self.dim == 1:
                x = np.atleast_2d(x).T
            else:
                x = np.atleast_2d(x)
        return self._pdf(x)

    def logpdf(self, x):
        if self.n_cl == 0:
            raise FIGAROException("You are trying to evaluate an empty mixture.\n If you are using the density_from_samples() method, you may want to evaluate the output of that method.")
        if len(np.shape(x)) < 2:
            if self.dim == 1:
                x = np.atleast_2d(x).T
            else:
                x = np.atleast_2d(x)
        return self._logpdf(x)

    @probit
    def _pdf(self, x):
        """
        Evaluate mixture at point(s) x
        
        Arguments:
            :np.ndarray x: point(s) to evaluate the mixture at
        
        Returns:
            :np.ndarray: mixture.pdf(x)
        """
        return self._pdf_probit(x) * np.exp(-probit_logJ(x, self.bounds, self.probit))

    @probit
    def _logpdf(self, x):
        """
        Evaluate log mixture at point(s) x
        
        Arguments:
            :np.ndarray x: point(s) to evaluate the mixture at
        
        Returns:
            :np.ndarray: mixture.logpdf(x)
        """
        return self._logpdf_probit(x) - probit_logJ(x, self.bounds, self.probit)

    def fast_pdf(self, x):
        """
        Fast pdf evaluation using FIGARO implementation of log_norm (JIT) rather than Numpy's.
        WARNING: it is meant to be used with MCMC samplers, therefore accepts only one point at a time.
        
        Arguments:
            :np.ndarray x: point to evaluate the mixture at
        
        Returns:
            :np.ndarray: mixture.pdf(x)
        """
        x = np.atleast_1d(x)
        if x.shape == (1,self.dim):
            return self._fast_pdf(x[0])
        elif x.shape == (self.dim,):
            return self._fast_pdf(x)
        else:
            raise FIGAROException("Please provide one point at a time.")

    def fast_logpdf(self, x):
        """
        Fast logpdf evaluation using FIGARO implementation of log_norm (JIT) rather than Numpy's.
        WARNING: it is meant to be used with MCMC samplers, therefore accepts only one point at a time.
        
        Arguments:
            :np.ndarray x: point to evaluate the mixture at
        
        Returns:
            :np.ndarray: mixture.pdf(x)
        """
        x = np.atleast_1d(x)
        if x.shape == (1,self.dim):
            return self._fast_logpdf(x[0])
        elif x.shape == (self.dim,):
            return self._fast_logpdf(x)
        else:
            raise FIGAROException("Please provide one point at a time.")

    @probit
    def _fast_pdf(self, x):
        """
        Evaluate mixture at point x
        
        Arguments:
            :np.ndarray x: point to evaluate the mixture at
        
        Returns:
            :np.ndarray: mixture.pdf(x)
        """
        return self._fast_pdf_probit(x) * np.exp(-probit_logJ(x, self.bounds, self.probit))

    @probit
    def _fast_logpdf(self, x):
        """
        Evaluate log mixture at point x
        
        Arguments:
            :np.ndarray x: point to evaluate the mixture at
        
        Returns:
            :np.ndarray: mixture.logpdf(x)
        """
        return self._fast_logpdf_probit(x) - probit_logJ(x, self.bounds, self.probit)

    def _fast_pdf_probit(self, x):
        """
        Evaluate mixture at point x in probit space
        
        Arguments:
            :np.ndarray x: point to evaluate the mixture at (in probit space)
        
        Returns:
            :np.ndarray: mixture.pdf(x)
        """
        return np.sum(np.array([w*np.exp(log_norm(x[0], mean, cov)) for mean, cov, w in zip(self.means, self.covs, self.w)]), axis = 0)

    def _fast_logpdf_probit(self, x):
        """
        Evaluate log mixture at point x in probit space
        
        Arguments:
            :np.ndarray x: point to evaluate the mixture at (in probit space)
        
        Returns:
            :np.ndarray: mixture.logpdf(x)
        """
        return logsumexp(np.array([w + log_norm(x[0], mean, cov) for mean, cov, w in zip(self.means, self.covs, self.log_w)]), axis = 0)

    @probit
    def _pdf_no_jacobian(self, x):
        """
        Evaluate mixture at point(s) x without jacobian
        
        Arguments:
            :np.ndarray x: point(s) to evaluate the mixture at
        
        Returns:
            :np.ndarray: mixture.pdf(x)
        """
        return self._pdf_probit(x)

    def _pdf_probit(self, x):
        """
        Evaluate mixture at point(s) x in probit space
        
        Arguments:
            :np.ndarray x: point(s) to evaluate the mixture at (in probit space)
        
        Returns:
            :np.ndarray: mixture.pdf(x)
        """
        return np.sum(np.array([w*mn(mean, cov).pdf(x) for mean, cov, w in zip(self.means, self.covs, self.w)]), axis = 0)

    @probit
    def _logpdf_no_jacobian(self, x):
        """
        Evaluate log mixture at point(s) x without jacobian
        
        Arguments:
            :np.ndarray x: point(s) to evaluate the mixture at
        
        Returns:
            :np.ndarray: mixture.logpdf(x)
        """
        return self._logpdf_probit(x)

    def _logpdf_probit(self, x):
        """
        Evaluate log mixture at point(s) x in probit space
        
        Arguments:
            :np.ndarray x: point(s) to evaluate the mixture at (in probit space)
        
        Returns:
            :np.ndarray: mixture.logpdf(x)
        """
        return logsumexp(np.array([w + mn(mean, cov).logpdf(x) for mean, cov, w in zip(self.means, self.covs, self.log_w)]), axis = 0)

    def cdf(self, x):
        if self.dim > 1:
            raise FIGAROException("cdf is provided only for 1-dimensional distributions")
        if len(np.shape(x)) < 2:
            x = np.atleast_2d(x).T
        return self._cdf(x)

    def logcdf(self, x):
        if self.dim > 1:
            raise FIGAROException("cdf is provided only for 1-dimensional distributions")
        if len(np.shape(x)) < 2:
            x = np.atleast_2d(x).T
        return self._logcdf(x)

    @probit
    def _cdf(self, x):
        """
        Evaluate mixture cdf at point(s) x
        
        Arguments:
            :np.ndarray x: point(s) to evaluate the mixture at
        
        Returns:
            :np.ndarray: mixture.cdf(x)
        """
        return np.sum(np.array([w*norm(mean[0], cov[0,0]).cdf(x) for mean, cov, w in zip(self.means, np.sqrt(self.covs), self.w)]), axis = 0)

    @probit
    def _logcdf(self, x):
        """
        Evaluate mixture log cdf at point(s) x
        
        Arguments:
            :np.ndarray x: point(s) to evaluate the mixture at
        
        Returns:
            :np.ndarray: mixture.logcdf(x)
        """
        return logsumexp(np.array([w + norm(mean[0], cov[0,0]).logcdf(x) for mean, cov, w in zip(self.means, np.sqrt(self.covs), self.log_w)]), axis = 0)

    @from_probit
    def rvs(self, n_samps):
        """
        Draw samples from mixture
        
        Arguments:
            :int n_samps: number of samples to draw
        
        Returns:
            :np.ndarray: samples
        """
        if self.n_cl == 0:
            raise FIGAROException("You are trying to draw samples from an empty mixture.\n If you are using the density_from_samples() method, you may want to draw samples from the output of that method.")
        return self._rvs_probit(n_samps)
        
    def _rvs_probit(self, n_samps):
        """
        Draw samples from mixture in probit space
        
        Arguments:
            :int n_samps: number of samples to draw
        
        Returns:
            :np.ndarray: samples in probit space
        """
        idx = np.random.choice(np.arange(self.n_cl), p = self.w, size = n_samps)
        ctr = Counter(idx)
        if self.dim > 1:
            samples = np.empty(shape = (1,self.dim))
            for i, n in zip(ctr.keys(), ctr.values()):
                samples = np.concatenate((samples, np.atleast_2d(mn(self.means[i], self.covs[i]).rvs(size = n))))
        else:
            samples = np.array([np.zeros(1)])
            for i, n in zip(ctr.keys(), ctr.values()):
                samples = np.concatenate((samples, np.atleast_2d(mn(self.means[i], self.covs[i]).rvs(size = n)).T))
        return np.array(samples[1:])

class mixture(_density):
    """
    Class to store a single draw from DPGMM/(H)DPGMM.
    Methods inherited from _density class.
    
    Arguments:
        :iterable means:    component means
        :iterable covs:     component covariances
        :np.ndarray w:      component weights
        :np.ndarray bounds: bounds of probit transformation
        :int dim:           number of dimensions
        :int n_cl:          number of clusters in the mixture
        :bool probit:       whether to use the probit transformation or not
    
    Returns:
        :mixture: instance of mixture class
    """
    def __init__(self, means, covs, w, bounds, dim, n_cl, n_pts, probit = True):
        self.means  = means
        self.covs   = covs
        self.w      = w
        self.log_w  = np.log(w)
        self.bounds = bounds
        self.dim    = dim
        self.n_cl   = n_cl
        self.n_pts  = n_pts
        self.probit = probit
    
    def marginalise(self, axis = -1):
        """
        Marginalise out one or more dimensions from the mixture.
        
        Arguments:
            :int or list of int axis:      axis to marginalise on
        
        Returns:
            :figaro.mixture.mixture: the marginalised mixture
        """
        return _marginalise(self, axis)
    
    def condition(self, vals, dims, norm = True):
        """
        Mixture conditioned on specific values of a subset of parameters.
        
        Arguments:
            :iterable vals:                value(s) to condition on
            :int or list of int dims:      dimension(s) associated with given vals (starting from 0)
            :bool norm:                    normalize the distribution
        
        Returns:
            :figaro.mixture.mixture: the conditioned mixture
        """
        v       = np.mean(self.bounds, axis = -1)
        v[dims] = vals
        return _condition(self, v, dims, norm)

#-------------------#
# Inference classes #
#-------------------#

class DPGMM(_density):
    """
    Class to infer a distribution given a set of samples.
    
    Arguments:
        :iterable bounds:     boundaries of the rectangle over which the distribution is defined. It should be in the format [[xmin, xmax],[ymin, ymax],...]
        :iterable prior_pars: NIW prior parameters (k, L, nu, mu)
        :double alpha0:       initial guess for concentration parameter
        :bool probit:         whether to use the probit transformation or not
    
    Returns:
        :DPGMM: instance of DPGMM class
    """
    def __init__(self, bounds,
                       prior_pars = None,
                       alpha0     = 1.,
                       probit     = True,
                       ):
        self.probit = probit
        self.bounds = np.atleast_2d(bounds)
        self.dim    = len(self.bounds)
        if prior_pars is not None:
            self.prior = prior(*prior_pars)
        else:
            self.prior = prior(*get_priors(bounds = self.bounds, probit = self.probit))
        self.alpha      = alpha0
        self.alpha_0    = alpha0
        self.mixture    = []
        self.w          = []
        self.log_w      = []
        self.N_list     = []
        self.n_cl       = 0
        self.n_pts      = 0

    def __call__(self, x):
        return self.pdf(x)

    def initialise(self, prior_pars = None):
        """
        Initialise the mixture to initial conditions.
        
        Arguments:
            :iterable prior_pars: NIW prior parameters (k, L, nu, mu). If None, old parameters are kept
        """
        self.alpha    = self.alpha_0
        self.mixture  = []
        self.w        = []
        self.log_w    = []
        self.N_list   = []
        self.n_cl     = 0
        self.n_pts    = 0
        if prior_pars is not None:
            self.prior = prior(*prior_pars)
        
    def _add_datapoint_to_component(self, x, ss):
        """
        Update component parameters after assigning a sample to a component
        
        Arguments:
            :np.ndarray x: sample
            :component ss: component to update
        
        Returns:
            :component: updated component
        """
        new_mean, new_S, new_N, new_mu, new_sigma = compute_component_suffstats(x, ss.mean, ss.S, ss.N, self.prior.mu, self.prior.k, self.prior.nu, self.prior.L)
        ss.mean  = new_mean
        ss.S     = new_S
        ss.N     = new_N
        ss.mu    = new_mu
        ss.sigma = new_sigma
        return ss
    
    def _log_predictive_likelihood(self, x, ss):
        """
        Compute log likelihood of drawing sample x from component ss given the samples that are already assigned to that component.
        
        Arguments:
            :np.ndarray x: sample
            :component ss: component to update
        
        Returns:
            :double: log Likelihood
        """
        if ss == "new":
            ss = component(np.zeros(self.dim), prior = self.prior)
            ss.N = 0.
        t_df, t_shape, mu_n = compute_t_pars(self.prior.k, self.prior.mu, self.prior.nu, self.prior.L, ss.mean, ss.S, ss.N, self.dim)
        return _student_t(df = t_df, t = x, mu = mu_n, sigma = t_shape, dim = self.dim)

    def _cluster_assignment_distribution(self, x):
        """
        Compute the marginal distribution of cluster assignment for each cluster.
        
        Arguments:
            :np.ndarray x: sample
        
        Returns:
            :dict: p_i for each component
        """
        scores = {}
        for i in list(np.arange(self.n_cl)) + ["new"]:
            if i == "new":
                ss = "new"
            else:
                ss = self.mixture[i]
            scores[i] = self._log_predictive_likelihood(x, ss)
            if ss == "new":
                scores[i] += np.log(self.alpha)
            else:
                scores[i] += np.log(ss.N)
        norm   = logsumexp(np.array([score for score in scores.values()]), b = np.ones(self.n_cl+1))
        scores = {cid: (np.exp(score - norm) if score < np.inf else 0) for cid, score in scores.items()} # score < inf checks also for NaNs
        return scores

    def _assign_to_cluster(self, x):
        """
        Assign the new sample x to an existing cluster or to a new cluster according to the marginal distribution of cluster assignment.
        
        Arguments:
            :np.ndarray x: sample
        """
        scores = self._cluster_assignment_distribution(x).items()
        labels, scores = zip(*scores)
        cid = np.random.choice(labels, p=scores)
        if cid == "new":
            self.mixture.append(component(x, prior = self.prior))
            self.N_list.append(1.)
            self.n_cl += 1
        else:
            self.mixture[int(cid)] = self._add_datapoint_to_component(x, self.mixture[int(cid)])
            self.N_list[int(cid)] += 1
        # Update weights
        self.w = np.array(self.N_list)
        self.w = self.w/self.w.sum()
        self.log_w = np.log(self.w)
        return
    
    def density_from_samples(self, samples):
        """
        Reconstruct the probability density from a set of samples.
        
        Arguments:
            :iterable samples: samples set
        
        Returns:
            :mixture: the inferred mixture
        """
        np.random.shuffle(samples)
        samples = np.ascontiguousarray(samples)
        for s in samples:
            self.add_new_point(s)
        d = self.build_mixture()
        self.initialise()
        return d
    
    @probit
    def add_new_point(self, x):
        """
        Update the probability density reconstruction adding a new sample
        
        Arguments:
            :np.ndarray x: sample
        """
        self.n_pts += 1
        self._assign_to_cluster(np.atleast_2d(x))
        self.alpha = update_alpha(self.alpha, self.n_pts, self.n_cl)

    def build_mixture(self):
        """
        Instances a mixture class representing the inferred distribution
        
        Returns:
            :mixture: the inferred distribution
        """
        if self.n_cl == 0:
            raise FIGAROException("You are trying to build an empty mixture - perhaps you called the initialise() method. If you are using the density_from_samples() method, the inferred mixture is returned by that method as an instance of mixture class.")
        return mixture(np.array([comp.mu for comp in self.mixture]), np.array([comp.sigma for comp in self.mixture]), np.array(self.w), self.bounds, self.dim, self.n_cl, self.n_pts, probit = self.probit)

    # Methods to overwrite _density methods
    def _rvs_probit(self, n_samps):
        """
        Draw samples from mixture in probit space
        
        Arguments:
            :int n_samps: number of samples to draw
        
        Returns:
            :np.ndarray: samples in probit space
        """
        idx = np.random.choice(np.arange(self.n_cl), p = self.w, size = n_samps)
        ctr = Counter(idx)
        if self.dim > 1:
            samples = np.empty(shape = (1,self.dim))
            for i, n in zip(ctr.keys(), ctr.values()):
                samples = np.concatenate((samples, np.atleast_2d(mn(self.mixture[i].mu, self.mixture[i].sigma).rvs(size = n))))
        else:
            samples = np.array([np.zeros(1)])
            for i, n in zip(ctr.keys(), ctr.values()):
                samples = np.concatenate((samples, np.atleast_2d(mn(self.mixture[i].mu, self.mixture[i].sigma).rvs(size = n)).T))
        return samples[1:]

    def _pdf_probit(self, x):
        """
        Evaluate mixture at point(s) x in probit space
        
        Arguments:
            :np.ndarray x: point(s) to evaluate the mixture at (in probit space)
        
        Returns:
            :np.ndarray: mixture.pdf(x)
        """
        return np.sum(np.array([w*mn(comp.mu, comp.sigma).pdf(x) for comp, w in zip(self.mixture, self.w)]), axis = 0)

    def _logpdf_probit(self, x):
        """
        Evaluate log mixture at point(s) x in probit space
        
        Arguments:
            :np.ndarray x: point(s) to evaluate the mixture at (in probit space)
        
        Returns:
            :np.ndarray: mixture.logpdf(x)
        """
        return logsumexp(np.array([w + mn(comp.mu, comp.sigma).logpdf(x) for comp, w in zip(self.mixture, self.log_w)]), axis = 0)

    def _fast_pdf_probit(self, x):
        """
        Evaluate mixture at point x in probit space
        
        Arguments:
            :np.ndarray x: point to evaluate the mixture at (in probit space)
        
        Returns:
            :np.ndarray: mixture.pdf(x)
        """
        return np.sum(np.array([w*np.exp(log_norm(x[0], comp.mean, comp.cov)) for comp, w in zip(self.mixture, self.w)]), axis = 0)

    def _fast_logpdf_probit(self, x):
        """
        Evaluate log mixture at point x in probit space
        
        Arguments:
            :np.ndarray x: point to evaluate the mixture at (in probit space)
        
        Returns:
            :np.ndarray: mixture.logpdf(x)
        """
        return logsumexp(np.array([w + log_norm(x[0], comp.mean, comp.cov) for comp, w in zip(self.mixture, self.log_w)]), axis = 0)

class HDPGMM(DPGMM):
    """
    Class to infer a distribution given a set of observations (each being a set of samples).
    Child of DPGMM class
    
    Arguments:
        :iterable bounds:  boundaries of the rectangle over which the distribution is defined. It should be in the format [[xmin, xmax],[ymin, ymax],...]
        :double alpha0:    initial guess for concentration parameter
        :double MC_draws:  number of MC draws for integral
        :bool probit:      whether to use the probit transformation or not
        :double sigma_min: lower bound for Jeffreys' prior on standard deviation
        :double sigma_max: upper bound for Jeffreys' prior on standard deviation
    
    Returns:
        :HDPGMM: instance of HDPGMM class
    """
    def __init__(self, bounds,
                       alpha0     = 1.,
                       prior_pars = None,
                       MC_draws   = 2e3,
                       probit     = True,
                       ):
        bounds   = np.atleast_2d(bounds)
        self.dim = len(bounds)
        super().__init__(bounds = bounds, alpha0 = alpha0, probit = probit)
        if prior_pars is not None:
            self.exp_sigma, self.a = prior_pars
        else:
            self.exp_sigma, self.a = get_priors(bounds = self.bounds, probit = self.probit, hierarchical = True)
        self.invgamma = invgamma(self.a)
        self.MC_draws = int(MC_draws)
        # For logsumexp_jit
        self.b_ones = np.ones(self.MC_draws)
        # MC samples
        self._draw_MC_samples()
        
    def initialise(self):
        """
        Initialise the mixture to initial conditions
        """
        super().initialise()
        self._draw_MC_samples()
    
    def _draw_MC_samples(self):
        """
        Draws MC samples for mu and sigma
        """
        self.sigma_MC = np.array([self.invgamma.rvs(self.MC_draws)*(self.exp_sigma[i]**2*(self.a+1)) for i in range(self.dim)]).T
        self.mu_MC    = np.random.uniform(low = self.bounds[:,0], high = self.bounds[:,1], size = (self.MC_draws, self.dim))
        if self.probit:
            self.mu_MC = transform_to_probit(self.mu_MC, self.bounds)
        if self.dim == 1:
            self.sigma_MC = self.sigma_MC.flatten()
            self.mu_MC = self.mu_MC.flatten()
        else:
            self.sigma_MC = np.array([invwishart(df = self.dim+2, scale = np.identity(self.dim)*cov).rvs() for cov in self.sigma_MC])
            
    def add_new_point(self, ev):
        """
        Update the probability density reconstruction adding a new sample
        
        Arguments:
            :iterable x: set of single-event draws from a DPGMM inference
        """
        self.n_pts += 1
        x = np.random.choice(ev)
        self._assign_to_cluster(x)
        self.alpha = update_alpha(self.alpha, self.n_pts, self.n_cl)

    def _cluster_assignment_distribution(self, x):
        """
        Compute the marginal distribution of cluster assignment for each cluster.
        
        Arguments:
            :np.ndarray x: sample
        
        Returns:
            :dict: p_i for each component
        """
        scores = {}
        logL_N = {}
        
        if self.dim == 1:
            logL_x = evaluate_mixture_MC_draws_1d(self.mu_MC, self.sigma_MC, x.means, x.covs, x.w)
        else:
            logL_x = evaluate_mixture_MC_draws(self.mu_MC, self.sigma_MC, x.means, x.covs, x.w)
        for i in list(np.arange(self.n_cl)) + ["new"]:
            if i == "new":
                ss = "new"
                logL_D = np.zeros(self.MC_draws)
            else:
                ss = self.mixture[i]
                logL_D = ss.logL_D
            scores[i] = logsumexp_jit(logL_D + logL_x, b = self.b_ones) - logsumexp_jit(logL_D, b = self.b_ones)
            logL_N[i] = logL_D + logL_x
            if ss == "new":
                scores[i] += np.log(self.alpha)
            else:
                scores[i] += np.log(ss.N)
        norm   = logsumexp(np.array([score for score in scores.values()]), b = np.ones(self.n_cl+1))
        scores = {cid: (np.exp(score - norm) if score < np.inf else 0)  for cid, score in scores.items()} # score < inf checks also for NaNs
        return scores, logL_N

    def _assign_to_cluster(self, x):
        """
        Assign the new sample x to an existing cluster or to a new cluster according to the marginal distribution of cluster assignment.
        
        Arguments:
            :np.ndarray x: sample
        """
        scores, logL_N = self._cluster_assignment_distribution(x)
        scores = scores.items()
        labels, scores = zip(*scores)
        try:
            cid = np.random.choice(labels, p=scores)
        except ValueError:
            cid = "new"
        if cid == "new":
            self.mixture.append(component_h(x, self.dim, self.prior, logL_N[cid], self.mu_MC, self.sigma_MC, self.b_ones))
            self.N_list.append(1.)
            self.n_cl += 1
        else:
            self.mixture[int(cid)] = self._add_datapoint_to_component(x, self.mixture[int(cid)], logL_N[int(cid)])
            self.N_list[int(cid)] += 1
        # Update weights
        self.w = np.array(self.N_list)
        self.w = self.w/self.w.sum()
        self.log_w = np.log(self.w)
        return

    def _add_datapoint_to_component(self, x, ss, logL_D):
        """
        Update component parameters after assigning a sample to a component
        
        Arguments:
            :np.ndarray x: sample
            :component ss: component to update
            :double logL_D: log Likelihood denominator
        
        Returns:
            :component: updated component
        """
        ss.events.append(x)
        ss.means.append(x.means)
        ss.covs.append(x.covs)
        ss.log_w.append(x.log_w)
        ss.logL_D = logL_D

        log_norm_D = logsumexp_jit(logL_D, self.b_ones)

        ss.mu    = np.average(self.mu_MC, weights = np.exp(logL_D - log_norm_D), axis = 0)
        ss.sigma = np.average(self.sigma_MC, weights = np.exp(logL_D - log_norm_D), axis = 0)
        if self.dim == 1:
            ss.mu = np.atleast_2d(ss.mu).T
            ss.sigma = np.atleast_2d(ss.sigma).T
        
        ss.N += 1
        return ss

    def density_from_samples(self, events):
        """
        Reconstruct the probability density from a set of samples.
        
        Arguments:
            :iterable samples: set of single-event draws from DPGMM
        
        Returns:
            :mixture: the inferred mixture
        """
        np.random.shuffle(events)
        for ev in events:
            self.add_new_point(ev)
        d = self.build_mixture()
        self.initialise()
        return d
