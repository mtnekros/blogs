"""
Question: 

Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].

The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

You must write an algorithm that runs in O(n) time and without using the division operation.

 

Example 1:

Input: nums = [1,2,3,4]
Output: [24,12,8,6]
Example 2:

Input: nums = [-1,1,0,-3,3]
Output: [0,0,9,0,0]
 

Constraints:

2 <= nums.length <= 105
-30 <= nums[i] <= 30
The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.
"""

def product_except_self(nums):
    """
    :type nums: List[int]
    :rtype: List[int]

    Calculates the left products first
    Calculate the right side products second
    And multiply them together to get the product except self
    """
    total = len(nums)
    prefix = 1
    res = []
    for i in range(total):
        res.append(prefix)
        prefix *= nums[i]
    post = 1
    for i in range(total-1, -1, -1):
        res[i] *= post
        post *= nums[i]
    return res

print(product_except_self([1,2,3,4]))
print(product_except_self([-1, 1, 0, -3, 3]))
