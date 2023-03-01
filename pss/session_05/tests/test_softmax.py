import pytest
import numpy as np
import torch
from scipy.special import softmax as scipy_softmax  # Correct implementation of softmax for testing purposes.

from source.softmax import stable_softmax



######################################################################
########################### SIMPLE TEST ##############################
######################################################################

# def test_softmax_numpy_simple_1d():
#     x, const = np.array([15]), 0.0
#     ground_truth = np.array([1.0])
#     assert stable_softmax(x=x, const=const) == ground_truth

######################################################################
######################################################################
######################################################################



######################################################################
########################## MULTIPLE TESTS ############################
######################################################################

# def test_softmax_numpy_multiple_1d():
#     x_inputs = [np.array([1.0, 1.0]), 
#                 np.array([2.0, 2.0]), 
#                 np.array([15.7, 15.7, 15.7, 15.7])]
#     consts = [0.0, 0.0, 0.0]
#     ground_truths = [np.array([0.5, 0.5]), 
#                      np.array([0.5, 0.5]), 
#                      np.array([0.25, 0.25, 0.25, 0.25])]
    
#     for idx in range(len(x_inputs)):
#         x, const = x_inputs[idx], consts[idx]
#         ground_truth = ground_truths[idx]
#         assert (stable_softmax(x=x, const=const) == ground_truth).all()
    
######################################################################
######################################################################
######################################################################



######################################################################
################# MULTIPLE TESTS (PARAMETRIZATION) ###################
######################################################################

# @pytest.mark.parametrize("x,const,ground_truth", [
#     (np.array([1.0, 1.0]), 0.0, np.array([0.5, 0.5])), 
#     (np.array([2.0, 2.0]), 3.9, np.array([0.5, 0.5])), 
#     (np.array([15.7, 15.7, 15.7, 15.7]), 5.2, np.array([0.25, 0.25, 0.25, 0.25])),
#     pytest.param(np.array([1.0, 1.0]), 0.0, np.array([0.4, 0.6]), marks=pytest.mark.xfail)
# ])
# def test_softmax_numpy_multiple_1d_param(x, const, ground_truth):
#     assert (stable_softmax(x=x, const=const) == ground_truth).all()
    
######################################################################
######################################################################
######################################################################



######################################################################
################## MULTIPLE TESTS (COMBINATIONS) #####################
######################################################################

# @pytest.mark.parametrize("x", [
#     np.array([1.0, 1.0]), 
#     np.array([2.0, 2.0]), 
#     np.array([15.7, 15.7, 15.7, 15.7])
# ])
# @pytest.mark.parametrize("const", [0.0, 3.9, 5.2])
# def test_softmax_numpy_multiple_1d_param_ext(x, const):
#     assert (stable_softmax(x=x, const=const) == scipy_softmax(x)).all()
    
######################################################################
######################################################################
######################################################################



######################################################################
########################### BAD INPUTS ###############################    
######################################################################

# def test_softmax_bad_inputs():
#     with pytest.raises(ValueError):
#         stable_softmax(x=[1, 2, 3], const=0.0)
    
######################################################################
######################################################################
######################################################################



######################################################################
#################### MULTIPLE TESTS (FIXTURES) #######################    
######################################################################

# @pytest.fixture(params=[
#     (1, 1), 
#     (2, 8), 
#     (3, 6)
# ])
# def random_numpy_input(request):
#     x = np.random.randn(*request.param)
#     const = np.max(x, axis=-1, keepdims=True)
#     return x, const


# def test_softmax_numpy_fixtures_shape(random_numpy_input):
#     assert stable_softmax(*random_numpy_input).shape == random_numpy_input[0].shape
    

# def test_softmax_numpy_fixtures_sum(random_numpy_input):
#     assert np.allclose(stable_softmax(*random_numpy_input).sum(axis=1), 
#                        np.ones(random_numpy_input[0].shape[0]))
    
######################################################################
######################################################################
######################################################################



######################################################################
####################### PYTORCH INPUTS ###############################
######################################################################

# @pytest.fixture(params=[
#     (1, 1), 
#     (2, 8), 
#     (3, 6)
# ])
# def random_torch_input(request):
#     x = torch.randn(size=request.param)
#     const = x.max(dim=-1, keepdims=True)[0]
#     return x, const


# def test_softmax_torch_fixtures_shape(random_torch_input):
#     assert stable_softmax(*random_torch_input).shape == random_torch_input[0].shape
    

# def test_softmax_torch_fixtures_sum(random_torch_input):
#     assert torch.allclose(stable_softmax(*random_torch_input).sum(dim=1), 
#                           torch.ones(random_torch_input[0].shape[0]))
    
######################################################################
######################################################################
######################################################################



######################################################################
########################### MARKERS ##################################
######################################################################

# Source: https://madewithml.com/courses/mlops/testing/#behavioral-testing
# @pytest.mark.skipif(
#     not torch.cuda.is_available(),
#     reason="Full training tests require a GPU."
# )
# def test_training():
#     # Usually takes a lot of time to finish.
#     print("Training...")
    

# @pytest.mark.small
# def test_softmax_simple_input():
#     x, const = np.array([15]), 0.0
#     ground_truth = np.array([1.0])
#     assert stable_softmax(x=x, const=const) == ground_truth

######################################################################
######################################################################
######################################################################