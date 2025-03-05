import time
import pandas as pd

from data_loader import load_dataset
from sequential import process_images_sequential
from threads import process_images_multithreading
from processes import process_images_multiprocessing
from feature_extraction import process_features_sequential, process_features_parallel
from models import train_and_evaluate_models
from preprocessing import process_image, show_filtered_images

def main():
    # === Data Loading ===
    dataset_path = '../datasets/brain_tumor_dataset/'
    yes_images, no_images = load_dataset(dataset_path)
    print(f"Number of 'yes' images: {len(yes_images)}")
    print(f"Number of 'no' images: {len(no_images)}")
    
    # === Display Example Filtered Image ===
    sample_image = yes_images[0]
    filtered = process_image(sample_image)
    show_filtered_images(filtered)
    
    # === Filtering the Dataset ===
    
    # sequential
    start_time_seq = time.time()
    yes_filtered_seq = process_images_sequential(yes_images)
    no_filtered_seq = process_images_sequential(no_images)
    end_time_seq = time.time()
    sequential_time = end_time_seq - start_time_seq
    print(f"Sequential execution time: {sequential_time:.4f} seconds")
    
    # multithreading
    num_workers = 6
    start_time_mt = time.time()
    yes_inputs_mt = process_images_multithreading(yes_images, num_workers)
    no_inputs_mt = process_images_multithreading(no_images, num_workers)
    end_time_mt = time.time()
    parallel_time_mt = end_time_mt - start_time_mt
    speedup_mt = sequential_time / parallel_time_mt
    efficiency_mt = speedup_mt / 6
    print(f"Multithreading execution time: {parallel_time_mt:.4f} seconds")
    print(f"Multithreading speedup: {speedup_mt:.4f}")
    print(f"Multithreading efficiency: {efficiency_mt:.4f}")
    
    # multiprocessing
    start_time_mp = time.time()
    yes_inputs_mp = process_images_multiprocessing(yes_images, num_workers)
    no_inputs_mp = process_images_multiprocessing(no_images, num_workers)
    end_time_mp = time.time()
    parallel_time_mp = end_time_mp - start_time_mp
    speedup_mp = sequential_time / parallel_time_mp
    efficiency_mp = speedup_mp / 6
    print(f"Multiprocessing execution time: {parallel_time_mp:.4f} seconds")
    print(f"Multiprocessing (concurrent.futures) speedup: {speedup_mp:.4f}")
    print(f"Multiprocessing (concurrent.futures) efficiency: {efficiency_mp:.4f}")
    
    # === Feature Extraction ===
    # Sequential feature extraction
    start_time_feat_seq = time.time()
    yes_features_seq = process_features_sequential(yes_filtered_seq, tumor_presence=1)
    no_features_seq = process_features_sequential(no_filtered_seq, tumor_presence=0)
    all_features_seq = yes_features_seq + no_features_seq
    df_features = pd.DataFrame(all_features_seq)
    print("Features DataFrame shape (sequential):", df_features.shape)
    end_time_feat_seq = time.time()
    print(f"Sequential feature extraction time: {end_time_feat_seq - start_time_feat_seq:.4f} seconds")
    
    # Parallel feature extraction
    start_time_feat_parallel = time.time()
    yes_features_parallel = process_features_parallel(yes_filtered_seq, tumor_presence=1)
    no_features_parallel = process_features_parallel(no_filtered_seq, tumor_presence=0)
    all_features_parallel = yes_features_parallel + no_features_parallel
    df_features = pd.DataFrame(all_features_parallel)
    print("Features DataFrame shape (parallel):", df_features.shape)
    end_time_feat_parallel = time.time()
    print(f"Parallel feature extraction time: {end_time_feat_parallel - start_time_feat_parallel:.4f} seconds")
    
    # === Model Training and Evaluation ===
    results = train_and_evaluate_models(df_features)
    for result in results:
        print(f"Model: {result['model']}")
        print(f"Accuracy: {result['accuracy']:.4f}")
        print(f"Precision: {result['precision']:.4f}")
        print(f"Recall: {result['recall']:.4f}")
        print(f"F1 Score: {result['f1_score']:.4f}")
        print("Confusion Matrix:")
        print(result['confusion_matrix'])
        print()

if __name__ == "__main__":
    main()
