from sklearn.decomposition import non_negative_factorization
import numpy as np
import pandas as pd 

# entry point
if __name__ == "__main__":
  print("starting Nonnegative Matrix Factorization tests")
  MAX_ITERATIONS = 5000
  RANK = 5

  using_real_data = False
  data = 0
  Dataset1_file = "Data/Dataset1/2024-12-02.csv"
  Dataset2_file = "Data/Dataset2/friend_jazz_drumming_frame0.csv"
  Dataset3_file = "Data/Dataset3/time_0.csv"
  if using_real_data:
    file_path = Dataset3_file  # Replace with the file to compute on
    df = pd.read_csv(file_path)
    if file_path[7] == '3':
      data = df.values # convert to numpy array
    else:
      data = df.iloc[:, 1:].values  # Remove the first column (index column) and convert to numpy array
  else:
    # Example data
    data = np.random.rand(500, 120)

  # ---------- ---------- ----------

  print(f"doing a low-rank-r with r={RANK} update...")
  # Apply NMF with MU solver
  print("FAST HALS\n-----")
  W, H, iters = non_negative_factorization(data, n_components=RANK, init='random', random_state=42, solver='cd', max_iter=MAX_ITERATIONS)

  # Frobenius Norm Error
  frobenius_error = np.linalg.norm(data - np.dot(W, H), 'fro')
  print("Frobenius Norm Error:", frobenius_error)

  print(f"W-shape: {W.shape}, H-shape: {H.shape}, Data-shape: {data.shape}")

  print(f"iterations: {iters}")
  #print(f"\n\nW: {W}\n----------\nH: {H}\n----------\n")

  # ---------- ---------- ----------

  # Apply NMF with CD solver
  print("multiplicative update\n-----")
  W, H, iters = non_negative_factorization(data, n_components=RANK, init='random', random_state=42, solver='mu', max_iter=MAX_ITERATIONS)  

  # Frobenius Norm Error
  frobenius_error = np.linalg.norm(data - np.dot(W, H), 'fro')
  print("Frobenius Norm Error:", frobenius_error)

  print(f"W-shape: {W.shape}, H-shape: {H.shape}, Data-shape: {data.shape}")

  print(f"iterations: {iters}")
  #print(f"\n\nW: {W}\n----------\nH: {H}\n----------\n")
