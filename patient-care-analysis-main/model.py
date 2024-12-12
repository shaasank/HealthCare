import pandas as pd
from sklearn.ensemble import RandomForestClassifier  # Placeholder for your model
import pickle
import networkx as nx

X_combined=pd.read_csv('./datasets/preprocesseddata.csv')
file_path = "./datasets/modified_dataset (1).csv"
data = pd.read_csv(file_path)
def load_model():
    # Initialize and return a dummy model
    model=pickle.load(open('./datasets/model_components2.pkl', 'rb'))
    return model


# Initialize a directed graph for the subset
G_subset = nx.DiGraph()

for _, row in data.iterrows():
    patient_id = f"Patient{row['PatientID']}"
    G_subset.add_node(patient_id, type='Patient')

    disease = row['Disease']
    G_subset.add_node(disease, type='Disease')

    G_subset.add_edge(patient_id, disease, type='SuffersFrom')

    symptoms = row['Symptoms'].split(',')

    for symptom in symptoms:
        symptom = symptom.strip()
        G_subset.add_node(symptom, type='Symptom')

        G_subset.add_edge(patient_id, symptom, type='HasSymptom')
        G_subset.add_edge(disease, symptom, type='AssociatedWith')


def extract_features(symptoms, graph):
    # Implement your feature extraction logic here.
    # For example, you could count the number of symptoms connected to the disease in the graph.
    features = []
    for symptom in symptoms:
        if symptom in graph:
            neighbors = graph[symptom]
            disease_neighbors = [n for n in neighbors if graph.nodes[n]['type'] == 'Disease']
            features.append(len(disease_neighbors))
        else:
            features.append(0)
    return features


# Dummy model for illustration


def predict_disease(symptoms):
    model=load_model()
    print(model)
    vectorizer=model['vectorizer']
    label_encoder=model['label_encoder']
    best_model=model['model']
    features = extract_features(symptoms.split(','), G_subset)
    features_df = pd.DataFrame([features]).fillna(0)
    features_vectorized = vectorizer.transform([', '.join(symptoms.split(','))]).toarray()
    features_vectorized_df = pd.DataFrame(features_vectorized, columns=vectorizer.get_feature_names_out())
    combined_features = pd.concat([features_df.reset_index(drop=True), features_vectorized_df], axis=1).reindex(columns=X_combined.columns, fill_value=0)
    disease_probs = best_model.predict_proba(combined_features)[0]

    top_3_indices = disease_probs.argsort()[-3:][::-1]
    top_3_diseases = label_encoder.inverse_transform(top_3_indices)

    top_disease = top_3_diseases[0]
    disease_info = data[data['Disease'] == top_disease].iloc[0]
    description = disease_info['Description']
    precautions = disease_info['Precautions']
    medications = disease_info['Medications']
    diet = disease_info['Diet']
    workout = disease_info['Workout']

    return top_3_diseases, description, precautions, medications, diet, workout

               

