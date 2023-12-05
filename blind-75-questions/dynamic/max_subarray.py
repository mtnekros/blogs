"""
152. Maximum Product Subarray
Medium
Given an integer array nums, find a subarray that has the largest product, and
return the product.

The test cases are generated so that the answer will fit in a 32-bit integer.


Example 1:

Input: nums = [2,3,-2,4]
Output: 6
Explanation: [2,3] has the largest product 6.
Example 2:

Input: nums = [-2,0,-1]
Output: 0
Explanation: The result cannot be 2, because [-2,-1] is not a subarray.
 

Constraints:

1 <= nums.length <= 2 * 104
-10 <= nums[i] <= 10
The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.
"""

def max_sub_array(nums):
    all_max = nums[0]
    cur_max, cur_min = 1, 1
    for n in nums:
        t1 = n*cur_max
        t2 = n*cur_min
        cur_max = max(t1, t2, n)
        cur_min = min(t1, t2, n)
        all_max = max(all_max, cur_max, cur_min)
        print(cur_max, cur_min, all_max)
    return all_max

print(max_sub_array([2,3,-2,4]))
print(max_sub_array([-2,0,4]))

