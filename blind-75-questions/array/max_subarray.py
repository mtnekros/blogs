# def max_sub_array(nums):
#     """
#     :type nums: List[int]
#     :rtype: int
#     """
#     curr_sum = 0
#     max_sum = nums[0]
#     i_start = 0
#     end_start = 0
#     for i,n in enumerate(nums):
#         if curr_sum < 0:
#             curr_sum = 0


def max_sub_array(nums):
    max_sum = nums[0]
    sum_ = 0
    for n in nums:
        print(sum_, n)
        sum_ += n
        if n > sum_:
            sum_ = n
        max_sum = max(max_sum, sum_)
        print("max_sum", max_sum)
    return max_sum

nums = [-4, -2, 1, 4, -1, 5]
nums = [1, -2, 1, 4, -1, 5, -10, -1, 1, 1, 1,1,9]

def cummulative_sum(nums):
    cs = []
    s = 0
    for n in nums:
        s += n
        cs.append(s)
    return cs

print(cummulative_sum(nums))
max_sub_array(nums)
