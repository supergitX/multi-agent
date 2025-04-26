def sort_list(input_list):
  """Sorts a list in ascending order.

  Args:
    input_list: The list to be sorted.

  Returns:
    A new list containing all items from the input list, sorted in 
    ascending order.  Returns an empty list if the input is None or empty.
  """
  if input_list is None:
      return []
  return sorted(input_list)