import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.decomposition import PCA
from transformers import AutoTokenizer, AutoModel
import torch
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Set seed for reproducibility
np.random.seed(42)
torch.manual_seed(42)

# Create the movie reviews dataset
def create_dataset():
    # Positive reviews
    positive_reviews = [
        "The cinematography in this film was breathtaking. Every scene felt like a painting.",
        "I was moved to tears by the protagonist's journey. Such a powerful story of resilience.",
        "This might be the director's best work yet. A perfect blend of humor and drama.",
        "The chemistry between the lead actors was electric. I believed every moment.",
        "A masterpiece of modern filmmaking. I couldn't look away for a second.",
        "The screenplay was brilliantly crafted, with dialogue that felt both realistic and poetic.",
        "I haven't enjoyed a movie this much in years. It's an instant classic.",
        "The plot twists were unexpected but made perfect sense within the story.",
        "The score elevated every scene, creating the perfect emotional landscape.",
        "A thought-provoking film that will stay with me for a long time.",
        "Visually stunning with performances that deserve all the awards.",
        "I was completely immersed from the opening scene to the credits.",
        "What a delightful surprise! This film exceeded all my expectations.",
        "The character development was handled with such care and nuance.",
        "A perfect example of how a simple story can be told in an extraordinary way.",
        "The editing was seamless, creating a perfect pace throughout.",
        "I laughed, I cried, I left the theater feeling inspired.",
        "This film reminded me why I fell in love with cinema in the first place.",
        "A perfect blend of style and substance that never feels pretentious.",
        "The ensemble cast delivered performances that felt authentic and compelling.",
        "This movie was a feast for the eyes with its gorgeous visuals and art direction.",
        "A heartwarming story that manages to avoid being saccharine or manipulative.",
        "I was completely enthralled by the world-building and attention to detail.",
        "The director's unique vision comes through in every carefully composed shot.",
        "An emotional rollercoaster in the best possible way. What a ride!",
        "The action sequences were choreographed brilliantly, adding real tension to the story.",
        "A film that respects its audience's intelligence while delivering pure entertainment.",
        "I can't remember the last time I was so thoroughly engaged with a movie.",
        "The writing was sharp, witty, and surprisingly profound at times.",
        "A perfect balance of humor, heart, and spectacle. Truly outstanding.",
        "I found myself completely invested in these characters and their journey.",
        "The practical effects added a tangible quality that CGI often lacks.",
        "A beautiful meditation on love, loss, and the human condition.",
        "This film takes bold creative risks that all pay off magnificently.",
        "The cinematography perfectly captured the emotional state of the characters.",
        "I was blown away by the attention to historical detail in this period piece.",
        "A perfect finale to the trilogy that honors everything that came before.",
        "The lead performance was transformative and completely captivating.",
        "This film manages to feel both timely and timeless. A remarkable achievement.",
        "The director's unique style elevates what could have been a standard genre film."
    ]
    
    # Negative reviews
    negative_reviews = [
        "The pacing was painfully slow, making the two-hour runtime feel like an eternity.",
        "Wooden acting and clichéd dialogue made it impossible to connect with any character.",
        "The plot holes were so numerous and glaring that they completely ruined the experience.",
        "This film tried to be profound but came across as pretentious and hollow.",
        "The CGI was embarrassingly bad, taking me out of the story repeatedly.",
        "A predictable, by-the-numbers story that brings nothing new to the genre.",
        "The tonal shifts were jarring, veering from comedy to drama with no cohesion.",
        "The characters were one-dimensional and their motivations made no sense.",
        "A disappointing waste of a talented cast and interesting premise.",
        "The script felt like a first draft that desperately needed more work.",
        "Overlong, overindulgent, and ultimately boring despite its flashy style.",
        "The director seemed more interested in showing off than telling a good story.",
        "Nonsensical plot twists undermined any investment in the narrative.",
        "The dialogue was so on-the-nose that it became unintentionally funny.",
        "A soulless cash grab that adds nothing to the original film.",
        "The soundtrack was overbearing and mismatched with the on-screen action.",
        "This film couldn't decide what it wanted to be, resulting in a muddled mess.",
        "The lead performance was so over-the-top that it became unintentionally comedic.",
        "A convoluted and confusing plot that collapses under its own weight.",
        "The humor fell completely flat, with joke after joke failing to land.",
        "This sequel undermines everything that made the original special.",
        "The directing was amateur at best, with basic filmmaking mistakes throughout.",
        "An incoherent story filled with contrivances and convenient coincidences.",
        "The film's messaging was heavy-handed to the point of being insulting.",
        "Terrible green screen effects that looked like they belonged in a student film.",
        "The editing was chaotic, making action sequences incomprehensible.",
        "This film has nothing new or interesting to say despite its runtime.",
        "The chemistry between the leads was nonexistent, making romance scenes painful.",
        "A shallow examination of complex issues that deserved more thoughtful treatment.",
        "The film was visually dark to the point where I couldn't see what was happening.",
        "Derivative and unoriginal, borrowing elements from better movies without understanding why they worked.",
        "The character motivations changed randomly to serve the plot rather than make sense.",
        "Annoying comic relief characters that detracted from any dramatic tension.",
        "A promising first act that completely falls apart in the second half.",
        "This felt like three different movies awkwardly stitched together.",
        "The practical effects looked cheap and unconvincing throughout.",
        "Artificial dialogue that no real human would ever speak.",
        "The film mistakes being loud and chaotic for being exciting.",
        "A disappointing adaptation that fails to capture what made the source material special.",
        "This movie thinks it's much smarter than it actually is."
    ]
    
    # Create dataset with labels (1 for positive, 0 for negative)
    reviews = positive_reviews + negative_reviews
    labels = [1] * len(positive_reviews) + [0] * len(negative_reviews)
    
    # Create DataFrame and shuffle
    df = pd.DataFrame({'text': reviews, 'label': labels})
    return df.sample(frac=1, random_state=42).reset_index(drop=True)

# Function to get BERT embeddings
def get_bert_embeddings(texts):
    # Load pre-trained model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
    model = AutoModel.from_pretrained('bert-base-uncased')
    
    # Set model to evaluation mode
    model.eval()
    
    # Use GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    model.to(device)
    
    # List to store embeddings
    embeddings = []
    
    # Process texts in batches
    batch_size = 8
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i+batch_size]
        
        # Tokenize the batch
        encoded = tokenizer(
            batch_texts,
            padding=True,
            truncation=True,
            max_length=128,
            return_tensors='pt'
        ).to(device)
        
        # Get embeddings without computing gradients
        with torch.no_grad():
            outputs = model(**encoded)
        
        # Get the [CLS] token embeddings (first token)
        batch_embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()
        embeddings.extend(batch_embeddings)
        
        # Print progress
        print(f"Processed {min(i+batch_size, len(texts))}/{len(texts)} reviews", end="\r")
    
    print()  # New line after progress display
    return np.array(embeddings)

# Function to visualize embeddings in 3D
def visualize_embeddings_3d(embeddings, labels):
    # Reduce dimensionality to 3D
    print("Reducing embeddings to 3D using PCA...")
    pca = PCA(n_components=3)
    embeddings_3d = pca.fit_transform(embeddings)
    
    # Create a 3D plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot points with different colors for different sentiments
    positive_mask = labels == 1
    negative_mask = labels == 0
    
    ax.scatter(
        embeddings_3d[positive_mask, 0],
        embeddings_3d[positive_mask, 1],
        embeddings_3d[positive_mask, 2],
        c='blue', marker='o', label='Positive', alpha=0.7, s=50
    )
    
    ax.scatter(
        embeddings_3d[negative_mask, 0],
        embeddings_3d[negative_mask, 1],
        embeddings_3d[negative_mask, 2],
        c='red', marker='x', label='Negative', alpha=0.7, s=50
    )
    
    # Add labels and legend
    ax.set_title('BERT Embeddings Visualization in 3D', fontsize=14)
    ax.set_xlabel('Principal Component 1')
    ax.set_ylabel('Principal Component 2')
    ax.set_zlabel('Principal Component 3')
    ax.legend()
    
    # Explained variance
    explained_variance = pca.explained_variance_ratio_
    print(f"Explained variance by the 3 principal components: {explained_variance}")
    print(f"Total explained variance: {sum(explained_variance):.4f}")
    
    # Add a text annotation with the explained variance
    ax.text2D(0.05, 0.95, f"Total explained variance: {sum(explained_variance):.2%}", 
              transform=ax.transAxes)
    
    # Show the plot
    plt.tight_layout()
    plt.show()
    
    return embeddings_3d, pca

def main():
    # Create dataset
    print("Creating movie reviews dataset...")
    df = create_dataset()
    print(f"Dataset shape: {df.shape}")
    print(f"Positive reviews: {df['label'].sum()}")
    print(f"Negative reviews: {len(df) - df['label'].sum()}")
    
    # Show a few examples
    print("\nExample positive review:")
    print(df[df['label'] == 1]['text'].iloc[0])
    print("\nExample negative review:")
    print(df[df['label'] == 0]['text'].iloc[0])
    
    # Generate BERT embeddings
    print("\nGenerating BERT embeddings...")
    embeddings = get_bert_embeddings(df['text'].tolist())
    print(f"Embeddings shape: {embeddings.shape}")
    
    # Visualize embeddings in 3D
    embeddings_3d, pca = visualize_embeddings_3d(embeddings, df['label'].values)
    
    # Split into train and test sets (75% train, 25% test)
    X_train, X_test, y_train, y_test = train_test_split(
        embeddings, df['label'], test_size=0.25, random_state=42, stratify=df['label']
    )
    print(f"\nTraining set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    
    # Train logistic regression model
    print("\nTraining logistic regression model...")
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)
    
    # Make predictions on test set
    y_pred = model.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy on test set: {accuracy:.4f}")
    
    # Print classification report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Negative', 'Positive']))
    
    # Print test predictions
    print("\nTest Predictions:")
    test_indices = np.arange(len(y_test))
    np.random.shuffle(test_indices)
    
    # Show the first 10 predictions after shuffling
    for i, idx in enumerate(test_indices[:10]):
        # Get the original index in the dataframe
        original_idx = y_test.index[idx]
        text = df.loc[original_idx, 'text']
        true_label = "Positive" if y_test.iloc[idx] == 1 else "Negative"
        pred_label = "Positive" if y_pred[idx] == 1 else "Negative"
        
        print(f"\nReview {i+1}:")
        # Truncate review text if too long for display
        if len(text) > 100:
            text = text[:97] + "..."
        print(f"Text: {text}")
        print(f"True sentiment: {true_label}")
        print(f"Predicted sentiment: {pred_label}")
        print(f"Correct: {'✓' if true_label == pred_label else '✗'}")
    
    # Plot decision boundary in 3D (optional, uses the first 3 principal components)
    # Note: This is a simplified visualization of the decision boundary
    print("\nVisualizing decision boundary in 3D space...")
    
    # Transform the embeddings to 3D
    X_train_3d = pca.transform(X_train)
    X_test_3d = pca.transform(X_test)
    
    # Train a new logistic regression on the 3D data
    model_3d = LogisticRegression(max_iter=1000, random_state=42)
    model_3d.fit(X_train_3d, y_train)
    
    # Make predictions using the 3D model
    y_pred_3d = model_3d.predict(X_test_3d)
    accuracy_3d = accuracy_score(y_test, y_pred_3d)
    
    print(f"Accuracy of 3D model: {accuracy_3d:.4f}")
    print(f"Difference from full model: {accuracy - accuracy_3d:.4f}")
    
    # Create a 3D plot showing test predictions
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot correct predictions
    correct_mask = y_pred_3d == y_test.values
    
    # Correct positive predictions
    correct_pos = np.logical_and(correct_mask, y_test.values == 1)
    ax.scatter(
        X_test_3d[correct_pos, 0],
        X_test_3d[correct_pos, 1],
        X_test_3d[correct_pos, 2],
        c='blue', marker='o', label='Correct Positive', alpha=0.7
    )
    
    # Correct negative predictions
    correct_neg = np.logical_and(correct_mask, y_test.values == 0)
    ax.scatter(
        X_test_3d[correct_neg, 0],
        X_test_3d[correct_neg, 1],
        X_test_3d[correct_neg, 2],
        c='red', marker='x', label='Correct Negative', alpha=0.7
    )
    
    # Incorrect predictions
    incorrect_mask = ~correct_mask
    
    # Incorrect predictions (should be positive but predicted negative)
    false_neg = np.logical_and(incorrect_mask, y_test.values == 1)
    ax.scatter(
        X_test_3d[false_neg, 0],
        X_test_3d[false_neg, 1],
        X_test_3d[false_neg, 2],
        c='blue', marker='s', edgecolors='black', linewidth=1.5,
        label='False Negative', alpha=0.7
    )
    
    # Incorrect predictions (should be negative but predicted positive)
    false_pos = np.logical_and(incorrect_mask, y_test.values == 0)
    ax.scatter(
        X_test_3d[false_pos, 0],
        X_test_3d[false_pos, 1],
        X_test_3d[false_pos, 2],
        c='red', marker='D', edgecolors='black', linewidth=1.5,
        label='False Positive', alpha=0.7
    )
    
    # Add labels and legend
    ax.set_title('Test Predictions in 3D BERT Embedding Space', fontsize=14)
    ax.set_xlabel('Principal Component 1')
    ax.set_ylabel('Principal Component 2')
    ax.set_zlabel('Principal Component 3')
    ax.legend()
    
    # Add accuracy text
    ax.text2D(0.05, 0.95, f"3D Model Accuracy: {accuracy_3d:.2%}", transform=ax.transAxes)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()