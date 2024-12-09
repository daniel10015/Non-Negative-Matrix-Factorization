from sklearn.decomposition import non_negative_factorization
import numpy as np

# entry point
if __name__ == "__main__":
  print("starting Nonnegative Matrix Factorization tests")
  MAX_ITERATIONS = 5000
  RANK = 5

  using_real_data = False
  data = 0
  if using_real_data:
    # get data here
    data = 1 # tmp
  else:
    # Example data
    data = np.random.rand(500, 120)

  # ---------- ---------- ----------

  # Apply NMF with MU solver
  print("FAST HALS\n-----")
  W, H, iters = non_negative_factorization(data, n_components=RANK, init='random', random_state=42, solver='cd', max_iter=MAX_ITERATIONS)

  # Frobenius Norm Error
  frobenius_error = np.linalg.norm(data - np.dot(W, H), 'fro')
  print("Frobenius Norm Error:", frobenius_error)

  print(f"iteratinos: {iters}\n\nW: {W}\n----------\nH: {H}\n----------\n")

  # ---------- ---------- ----------

  # Apply NMF with CD solver
  print("multiplicative update\n-----")
  W, H, iters = non_negative_factorization(data, n_components=RANK, init='random', random_state=42, solver='mu', max_iter=MAX_ITERATIONS)
  

  # Frobenius Norm Error
  frobenius_error = np.linalg.norm(data - np.dot(W, H), 'fro')
  print("Frobenius Norm Error:", frobenius_error)

  print(f"iteratinos: {iters}\n\nW: {W}\n----------\nH: {H}\n----------\n")
