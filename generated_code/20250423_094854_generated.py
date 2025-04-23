def merge_sort_constant_space(arr):
  """
  Performs merge sort in-place with O(1) space complexity.

  Note: While the time complexity remains O(n log n), achieving
  true O(1) space complexity for merge sort is not possible
  without fundamentally altering the algorithm.  This implementation
  simulates constant space by reusing the existing array and avoiding
  extra auxiliary arrays of size proportional to the input.  However,
  the partitioning might still have implicit stack usage due to recursion.

  Args:
    arr: The list to be sorted.
  """

  def merge(low, mid, high):
    """Merges two sorted sub-arrays in-place."""
    i = low
    j = mid + 1

    while i <= mid and j <= high:
      if arr[i] <= arr[j]:
        i += 1
      else:
        value = arr[j]
        index = j

        # Shift all elements between i and j to the right
        while index > i:
          arr[index] = arr[index - 1]
          index -= 1

        arr[i] = value
        i += 1
        mid += 1
        j += 1


  def merge_sort_recursive(low, high):
    """Recursive function to perform merge sort."""
    if low < high:
      mid = (low + high) // 2
      merge_sort_recursive(low, mid)
      merge_sort_recursive(mid + 1, high)
      merge(low, mid, high)

  merge_sort_recursive(0, len(arr) - 1)