from typing import Union
import numpy as np
import torch


def stable_softmax(x: Union[np.ndarray, torch.Tensor], 
                   const: Union[float, np.ndarray, torch.Tensor]) -> Union[np.ndarray, torch.Tensor]:
    """Calculates stable softmax of x.
    
    Arguments:
        x: Either numpy array or torch tensor.
        const: Constant value.
        
    Returns:
        softmax(x-const).
    """
    if isinstance(x, np.ndarray):
        z = x - const
        numerator = np.exp(z)
        denominator = np.sum(numerator, axis=-1, keepdims=True)
        softmax = np.exp(z) / denominator
    elif isinstance(x, torch.Tensor):
        z = x - const
        numerator = z.exp()
        denominator = numerator.sum(dim=-1, keepdims=True)
        softmax = numerator / denominator
    else:
        raise ValueError(f"Expected x to be of type either np.ndarray or torch.Tensor but got {type(x)}.")
    return softmax
