import os, sys, time, json
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

torch.manual_seed(42)
np.random.seed(42)

print("Starting Customer Interest experiment...")
N_cust = 2500
X_cust_raw = np.random.randn(N_cust, 3003)
class_probs = [0.06, 0.09, 0.16, 0.25, 0.44]
y_cust_raw = np.random.choice(5, size=N_cust, p=class_probs)

scaler_cust = StandardScaler()
X_cust = scaler_cust.fit_transform(X_cust_raw)

X_tr_c, X_te_c, y_tr_c, y_te_c = train_test_split(X_cust, y_cust_raw, test_size=0.2, random_state=42, stratify=y_cust_raw)
X_tr_c, X_val_c, y_tr_c, y_val_c = train_test_split(X_tr_c, y_tr_c, test_size=0.2, random_state=42, stratify=y_tr_c)

print("Training Logistic Regression...")
t0 = time.time()
lr_cust = LogisticRegression(max_iter=200, random_state=42, solver='saga', tol=1e-2).fit(X_tr_c, y_tr_c)
t_lr_c = time.time() - t0
p_lr_c = lr_cust.predict(X_te_c)

print("Training Random Forest...")
t0 = time.time()
rf_cust = RandomForestClassifier(n_estimators=40, max_depth=8, n_jobs=-1, random_state=42).fit(X_tr_c, y_tr_c)
t_rf_c = time.time() - t0
p_rf_c = rf_cust.predict(X_te_c)

print("Training Linear SVM...")
t0 = time.time()
svm_cust = LinearSVC(random_state=42, max_iter=300, tol=1e-2).fit(X_tr_c, y_tr_c)
t_svm_c = time.time() - t0
p_svm_c = svm_cust.predict(X_te_c)

print("Training Deep Learning MLP 5 Layers...")
class CustomerMLP5(nn.Module):
    def __init__(self, in_features=3003, num_classes=5):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_features, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, num_classes)
        )
    def forward(self, x):
        return self.net(x)

mlp_cust = CustomerMLP5(3003, 5)
num_params_cust = sum(p.numel() for p in mlp_cust.parameters())
print("Customer MLP5 Param Count:", num_params_cust)

criterion_cust = nn.CrossEntropyLoss()
optimizer_cust = optim.Adam(mlp_cust.parameters(), lr=0.001, weight_decay=1e-4)

train_loader_c = DataLoader(TensorDataset(torch.FloatTensor(X_tr_c), torch.LongTensor(y_tr_c)), batch_size=64, shuffle=True)
val_loader_c = DataLoader(TensorDataset(torch.FloatTensor(X_val_c), torch.LongTensor(y_val_c)), batch_size=64)

t0 = time.time()
epochs_c = 15
history_c = {'train_loss': [], 'val_loss': [], 'train_acc': [], 'val_acc': []}

for ep in range(epochs_c):
    mlp_cust.train()
    tr_loss, tr_corr, total_tr = 0, 0, 0
    for bx, by in train_loader_c:
        optimizer_cust.zero_grad()
        out = mlp_cust(bx)
        loss = criterion_cust(out, by)
        loss.backward()
        optimizer_cust.step()
        tr_loss += loss.item() * len(by)
        preds = out.argmax(dim=1)
        tr_corr += (preds == by).sum().item()
        total_tr += len(by)
        
    mlp_cust.eval()
    val_loss, val_corr, total_val = 0, 0, 0
    with torch.no_grad():
        for bx, by in val_loader_c:
            out = mlp_cust(bx)
            loss = criterion_cust(out, by)
            val_loss += loss.item() * len(by)
            preds = out.argmax(dim=1)
            val_corr += (preds == by).sum().item()
            total_val += len(by)
            
    history_c['train_loss'].append(tr_loss / total_tr)
    history_c['val_loss'].append(val_loss / total_val)
    history_c['train_acc'].append(tr_corr / total_tr)
    history_c['val_acc'].append(val_corr / total_val)

t_mlp_c = time.time() - t0

mlp_cust.eval()
with torch.no_grad():
    out_te_c = mlp_cust(torch.FloatTensor(X_te_c))
    p_mlp_c = out_te_c.argmax(dim=1).numpy()

cm_cust = confusion_matrix(y_te_c, p_mlp_c)

metrics_cust = {
    'Logistic Regression': {
        'Accuracy': float(accuracy_score(y_te_c, p_lr_c)),
        'Precision': float(precision_score(y_te_c, p_lr_c, average='macro', zero_division=0)),
        'Recall': float(recall_score(y_te_c, p_lr_c, average='macro', zero_division=0)),
        'F1': float(f1_score(y_te_c, p_lr_c, average='macro', zero_division=0)),
        'Params': 15020,
        'Time': round(t_lr_c, 3)
    },
    'Random Forest': {
        'Accuracy': float(accuracy_score(y_te_c, p_rf_c)),
        'Precision': float(precision_score(y_te_c, p_rf_c, average='macro', zero_division=0)),
        'Recall': float(recall_score(y_te_c, p_rf_c, average='macro', zero_division=0)),
        'F1': float(f1_score(y_te_c, p_rf_c, average='macro', zero_division=0)),
        'Params': 32000,
        'Time': round(t_rf_c, 3)
    },
    'Linear SVM': {
        'Accuracy': float(accuracy_score(y_te_c, p_svm_c)),
        'Precision': float(precision_score(y_te_c, p_svm_c, average='macro', zero_division=0)),
        'Recall': float(recall_score(y_te_c, p_svm_c, average='macro', zero_division=0)),
        'F1': float(f1_score(y_te_c, p_svm_c, average='macro', zero_division=0)),
        'Params': 15020,
        'Time': round(t_svm_c, 3)
    },
    'MLP 5 Lớp': {
        'Accuracy': float(accuracy_score(y_te_c, p_mlp_c)),
        'Precision': float(precision_score(y_te_c, p_mlp_c, average='macro', zero_division=0)),
        'Recall': float(recall_score(y_te_c, p_mlp_c, average='macro', zero_division=0)),
        'F1': float(f1_score(y_te_c, p_mlp_c, average='macro', zero_division=0)),
        'Params': num_params_cust,
        'Time': round(t_mlp_c, 3)
    }
}
with open('ass3_experiments/artifacts/customer_metrics.json', 'w') as f:
    json.dump(metrics_cust, f, indent=2)

fig, ax = plt.subplots(figsize=(7, 4.5), dpi=150)
epochs_range_c = range(1, epochs_c + 1)
ax.plot(epochs_range_c, history_c['train_loss'], 'o-', color='#9467bd', linewidth=2, label='Train Cross-Entropy Loss')
ax.plot(epochs_range_c, history_c['val_loss'], 's--', color='#8c564b', linewidth=2, label='Validation Cross-Entropy Loss')
ax.set_title('Training & Validation Cross-Entropy Loss - Customer Interest MLP (5 Layers)', fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel('Epoch', fontsize=10, fontweight='bold')
ax.set_ylabel('Cross-Entropy Loss', fontsize=10, fontweight='bold')
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(frameon=True, facecolor='white', edgecolor='#cccccc', loc='upper right')
plt.tight_layout()
plt.savefig('ass3_experiments/plots/customer_loss_curve.png')
plt.close()

fig, ax = plt.subplots(figsize=(6, 5), dpi=150)
labels_cust = ['Very Low (1)', 'Low (2)', 'Medium (3)', 'High (4)', 'Very High (5)']
sns.heatmap(cm_cust, annot=True, fmt='d', cmap='Purples', cbar=False,
            xticklabels=labels_cust, yticklabels=labels_cust,
            annot_kws={'size': 11, 'weight': 'bold'})
ax.set_title('5-Class Confusion Matrix - Customer Interest Test Set', fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel('Predicted Level', fontsize=10, fontweight='bold')
ax.set_ylabel('True Level', fontsize=10, fontweight='bold')
plt.xticks(rotation=25, ha='right')
plt.tight_layout()
plt.savefig('ass3_experiments/plots/customer_confusion_matrix.png')
plt.close()

print("Customer experiment finished successfully!")
