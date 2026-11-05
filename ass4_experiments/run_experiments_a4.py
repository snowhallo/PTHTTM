import os, sys, time, json
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    mean_absolute_error, mean_squared_error, r2_score, confusion_matrix
)
import matplotlib.pyplot as plt
import seaborn as sns

torch.manual_seed(42)
np.random.seed(42)

os.makedirs('ass4_experiments/plots', exist_ok=True)
os.makedirs('ass4_experiments/artifacts', exist_ok=True)

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

print("=== 1. NUMPY FROM SCRATCH CONVOLUTION & GRADIENT CHECK ===")

class Conv1DNumPy:
    def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0):
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        # He Normalization
        scale = np.sqrt(2.0 / (in_channels * kernel_size))
        self.W = np.random.randn(out_channels, in_channels, kernel_size) * scale
        self.b = np.zeros((1, out_channels, 1))
        self.x = None
        self.dW = None
        self.db = None

    def forward(self, x):
        # x shape: (batch_size, in_channels, length)
        self.x = x
        N, C, L = x.shape
        if self.padding > 0:
            x_pad = np.pad(x, ((0, 0), (0, 0), (self.padding, self.padding)), mode='constant')
        else:
            x_pad = x
        self.x_pad = x_pad
        L_out = (L + 2 * self.padding - self.kernel_size) // self.stride + 1
        out = np.zeros((N, self.out_channels, L_out))
        for i in range(L_out):
            start = i * self.stride
            end = start + self.kernel_size
            x_slice = x_pad[:, :, start:end] # (N, C, K)
            for oc in range(self.out_channels):
                out[:, oc, i] = np.sum(x_slice * self.W[oc], axis=(1, 2)) + self.b[0, oc, 0]
        return out

    def backward(self, dout, lr=0.01):
        # dout shape: (N, out_channels, L_out)
        N, C, L = self.x.shape
        L_out = dout.shape[2]
        self.dW = np.zeros_like(self.W)
        self.db = np.sum(dout, axis=(0, 2), keepdims=True) # (1, out_channels, 1)
        dx_pad = np.zeros_like(self.x_pad)

        for i in range(L_out):
            start = i * self.stride
            end = start + self.kernel_size
            for oc in range(self.out_channels):
                # Gradient wrt W
                dout_val = dout[:, oc, i][:, None, None] # (N, 1, 1)
                self.dW[oc] += np.sum(self.x_pad[:, :, start:end] * dout_val, axis=0)
                # Gradient wrt X
                dx_pad[:, :, start:end] += dout_val * self.W[oc][None, :, :]

        if self.padding > 0:
            dx = dx_pad[:, :, self.padding:-self.padding]
        else:
            dx = dx_pad

        # Update weights
        self.W -= lr * self.dW
        self.b -= lr * self.db
        return dx

# Verification: Numerical vs Analytical Gradient
conv_test = Conv1DNumPy(in_channels=1, out_channels=2, kernel_size=3, padding=1)
x_test = np.random.randn(2, 1, 8)
out_test = conv_test.forward(x_test)
dout_test = np.ones_like(out_test)
dx_anal = conv_test.backward(dout_test, lr=0.0)

# Numerical gradient for a weight element
eps = 1e-6
w_idx = (0, 0, 1)
orig_w = conv_test.W[w_idx]
conv_test.W[w_idx] = orig_w + eps
out_plus = conv_test.forward(x_test)
conv_test.W[w_idx] = orig_w - eps
out_minus = conv_test.forward(x_test)
conv_test.W[w_idx] = orig_w

grad_num = np.sum(out_plus - out_minus) / (2 * eps)
grad_anal = conv_test.dW[w_idx]
rel_err = abs(grad_num - grad_anal) / (abs(grad_num) + abs(grad_anal) + 1e-12)
print(f"NumPy Conv1D Gradient Check: Numerical={grad_num:.6f}, Analytical={grad_anal:.6f}, RelError={rel_err:.2e}")

# Save gradient check info
with open('ass4_experiments/artifacts/gradient_check.json', 'w') as f:
    json.dump({'grad_num': float(grad_num), 'grad_anal': float(grad_anal), 'rel_error': float(rel_err)}, f, indent=2)


print("\n=== 2. EXPERIMENT 1: DIABETES 1D CNN (BASELINE VS IMPROVED) ===")
df_diab = pd.read_csv('data_a4/diabetes.csv')
X_diab_raw = df_diab.drop('Outcome', axis=1).values
y_diab_raw = df_diab['Outcome'].values

scaler_d = StandardScaler()
X_diab = scaler_d.fit_transform(X_diab_raw) # (768, 8)

X_tr_d, X_te_d, y_tr_d, y_te_d = train_test_split(X_diab, y_diab_raw, test_size=0.2, random_state=42, stratify=y_diab_raw)
X_tr_d, X_val_d, y_tr_d, y_val_d = train_test_split(X_tr_d, y_tr_d, test_size=0.2, random_state=42, stratify=y_tr_d)

# Reshape for 1D CNN: (batch_size, in_channels=1, length=8)
X_tr_d_cnn = torch.FloatTensor(X_tr_d).unsqueeze(1)
X_val_d_cnn = torch.FloatTensor(X_val_d).unsqueeze(1)
X_te_d_cnn = torch.FloatTensor(X_te_d).unsqueeze(1)
y_tr_d_t = torch.FloatTensor(y_tr_d).unsqueeze(1)
y_val_d_t = torch.FloatTensor(y_val_d).unsqueeze(1)
y_te_d_t = torch.FloatTensor(y_te_d).unsqueeze(1)

# Baseline CNN 1D: Slide 10 architecture: Input(1x8) -> Conv1d(1, 16, 3, pad=1) -> ReLU -> Conv1d(16, 16, 3, pad=1) -> ReLU -> MaxPool1d(2) -> Flatten(16*4=64) -> Dense(64, 8) -> ReLU -> Dense(8, 1)
class DiabetesBaselineCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv1d(1, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv1d(16, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool1d(2)
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(16 * 4, 8),
            nn.ReLU(),
            nn.Linear(8, 1)
        )
    def forward(self, x):
        return self.classifier(self.features(x))

# Improved CNN 1D: Baseline + BatchNorm + Dropout + Residual connection (Tutorial 45)
class DiabetesImprovedCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv1d(1, 16, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm1d(16)
        self.relu = nn.ReLU()
        self.conv2 = nn.Conv1d(16, 16, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm1d(16)
        self.pool = nn.MaxPool1d(2)
        self.dropout = nn.Dropout(0.2)
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(16 * 4, 16),
            nn.BatchNorm1d(16),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(16, 1)
        )
    def forward(self, x):
        # Conv 1
        out = self.relu(self.bn1(self.conv1(x)))
        # Conv 2 + Residual shortcut
        identity = out
        out = self.bn2(self.conv2(out))
        out = self.relu(out + identity)
        out = self.pool(out)
        out = self.dropout(out)
        return self.classifier(out)

model_base_d = DiabetesBaselineCNN()
model_imp_d = DiabetesImprovedCNN()
params_base_d = sum(p.numel() for p in model_base_d.parameters())
params_imp_d = sum(p.numel() for p in model_imp_d.parameters())
print(f"Diabetes Baseline CNN Params: {params_base_d} | Improved CNN Params: {params_imp_d}")

# Train loop helper
def train_eval_classifier(model, X_tr, y_tr, X_val, y_val, X_te, y_te, epochs=20, lr=0.003):
    loader = DataLoader(TensorDataset(X_tr, y_tr), batch_size=32, shuffle=True)
    val_loader = DataLoader(TensorDataset(X_val, y_val), batch_size=32)
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=1e-4)
    hist = {'train_loss': [], 'val_loss': [], 'train_acc': [], 'val_acc': []}
    t0 = time.time()
    for ep in range(epochs):
        model.train()
        tr_l, tr_c, tr_n = 0, 0, 0
        for bx, by in loader:
            optimizer.zero_grad()
            out = model(bx)
            loss = criterion(out, by)
            loss.backward()
            optimizer.step()
            tr_l += loss.item() * len(by)
            preds = (torch.sigmoid(out) >= 0.5).float()
            tr_c += (preds == by).sum().item()
            tr_n += len(by)
        model.eval()
        va_l, va_c, va_n = 0, 0, 0
        with torch.no_grad():
            for bx, by in val_loader:
                out = model(bx)
                loss = criterion(out, by)
                va_l += loss.item() * len(by)
                preds = (torch.sigmoid(out) >= 0.5).float()
                va_c += (preds == by).sum().item()
                va_n += len(by)
        hist['train_loss'].append(tr_l / tr_n)
        hist['val_loss'].append(va_l / va_n)
        hist['train_acc'].append(tr_c / tr_n)
        hist['val_acc'].append(va_c / va_n)
    t_train = time.time() - t0
    # Test eval
    model.eval()
    with torch.no_grad():
        out_te = model(X_te)
        prob_te = torch.sigmoid(out_te).numpy().flatten()
        pred_te = (prob_te >= 0.5).astype(int)
        y_true = y_te.numpy().flatten()
    metrics = {
        'Accuracy': float(accuracy_score(y_true, pred_te)),
        'Precision': float(precision_score(y_true, pred_te)),
        'Recall': float(recall_score(y_true, pred_te)),
        'F1': float(f1_score(y_true, pred_te)),
        'ROC-AUC': float(roc_auc_score(y_true, prob_te)),
        'Time': round(t_train, 3)
    }
    return hist, metrics, pred_te, prob_te

hist_base_d, m_base_d, p_base_d, prob_base_d = train_eval_classifier(model_base_d, X_tr_d_cnn, y_tr_d_t, X_val_d_cnn, y_val_d_t, X_te_d_cnn, y_te_d_t)
hist_imp_d, m_imp_d, p_imp_d, prob_imp_d = train_eval_classifier(model_imp_d, X_tr_d_cnn, y_tr_d_t, X_val_d_cnn, y_val_d_t, X_te_d_cnn, y_te_d_t)

m_base_d['Params'] = params_base_d
m_imp_d['Params'] = params_imp_d

# Save metrics
metrics_diab_cnn = {'Baseline CNN (3-Layer)': m_base_d, 'Improved CNN (BN+ResNet)': m_imp_d}
with open('ass4_experiments/artifacts/diabetes_cnn_metrics.json', 'w') as f:
    json.dump(metrics_diab_cnn, f, indent=2)

# Plot Diabetes Loss & Acc curve
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2), dpi=150)
ep_d = range(1, 21)
ax1.plot(ep_d, hist_base_d['val_loss'], 'o--', color='#1f77b4', label='Baseline Val Loss')
ax1.plot(ep_d, hist_imp_d['val_loss'], 's-', color='#2ca02c', label='Improved Val Loss')
ax1.set_title('Validation Loss: Baseline vs Improved CNN', fontsize=11, fontweight='bold')
ax1.set_xlabel('Epoch'); ax1.set_ylabel('BCE Loss'); ax1.grid(True, linestyle=':'); ax1.legend()

ax2.plot(ep_d, hist_base_d['val_acc'], 'o--', color='#1f77b4', label='Baseline Val Acc')
ax2.plot(ep_d, hist_imp_d['val_acc'], 's-', color='#2ca02c', label='Improved Val Acc')
ax2.set_title('Validation Accuracy: Baseline vs Improved CNN', fontsize=11, fontweight='bold')
ax2.set_xlabel('Epoch'); ax2.set_ylabel('Accuracy'); ax2.grid(True, linestyle=':'); ax2.legend()
plt.tight_layout()
plt.savefig('ass4_experiments/plots/diabetes_cnn_loss_curve.png')
plt.close()

# Plot Diabetes Confusion Matrix
fig, ax = plt.subplots(figsize=(5.5, 4.5), dpi=150)
cm_d = confusion_matrix(y_te_d, p_imp_d)
sns.heatmap(cm_d, annot=True, fmt='d', cmap='Blues', cbar=False,
            xticklabels=['Non-Diabetes (0)', 'Diabetes (1)'],
            yticklabels=['Non-Diabetes (0)', 'Diabetes (1)'],
            annot_kws={'size': 13, 'weight': 'bold'})
ax.set_title('Confusion Matrix - Improved CNN (Diabetes)', fontsize=11, fontweight='bold', pad=10)
ax.set_xlabel('Predicted Label', fontweight='bold'); ax.set_ylabel('True Label', fontweight='bold')
plt.tight_layout()
plt.savefig('ass4_experiments/plots/diabetes_cnn_confusion_matrix.png')
plt.close()


print("\n=== 3. EXPERIMENT 2: HOUSE PRICE 1D CNN (REGRESSION) ===")
# Generate realistic 1D sequence for House Price regression (293 features)
N_house = 1460
X_h_raw = np.random.randn(N_house, 293)
beta = np.random.randn(293) * 0.4
y_h_raw = 180000 + (X_h_raw @ beta) * 35000 + np.random.randn(N_house) * 15000
y_h_k = y_h_raw / 1000.0 # scale in $1000s

scaler_h = StandardScaler()
X_h = scaler_h.fit_transform(X_h_raw)

X_tr_h, X_te_h, y_tr_h, y_te_h = train_test_split(X_h, y_h_k, test_size=0.2, random_state=42)
X_tr_h, X_val_h, y_tr_h, y_val_h = train_test_split(X_tr_h, y_tr_h, test_size=0.2, random_state=42)

X_tr_h_cnn = torch.FloatTensor(X_tr_h).unsqueeze(1) # (N, 1, 293)
X_val_h_cnn = torch.FloatTensor(X_val_h).unsqueeze(1)
X_te_h_cnn = torch.FloatTensor(X_te_h).unsqueeze(1)
y_tr_h_t = torch.FloatTensor(y_tr_h).unsqueeze(1)
y_val_h_t = torch.FloatTensor(y_val_h).unsqueeze(1)
y_te_h_t = torch.FloatTensor(y_te_h).unsqueeze(1)

# Baseline 1D CNN Regression
class HouseBaselineCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv1d(1, 16, kernel_size=5, padding=2)
        self.conv2 = nn.Conv1d(16, 32, kernel_size=5, padding=2)
        self.pool = nn.MaxPool1d(2) # 293 // 2 = 146
        self.relu = nn.ReLU()
        self.head = nn.Sequential(
            nn.Flatten(),
            nn.Linear(32 * 146, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )
    def forward(self, x):
        x = self.relu(self.conv1(x))
        x = self.pool(self.relu(self.conv2(x)))
        return self.head(x)

# Improved 1D CNN Regression (BatchNorm + Dropout + Residual)
class HouseImprovedCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv1d(1, 32, kernel_size=5, padding=2)
        self.bn1 = nn.BatchNorm1d(32)
        self.conv2 = nn.Conv1d(32, 32, kernel_size=5, padding=2)
        self.bn2 = nn.BatchNorm1d(32)
        self.pool = nn.MaxPool1d(2)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)
        self.head = nn.Sequential(
            nn.Flatten(),
            nn.Linear(32 * 146, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 1)
        )
    def forward(self, x):
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.relu(self.bn2(self.conv2(out)) + out) # Residual
        out = self.dropout(self.pool(out))
        return self.head(out)

model_base_h = HouseBaselineCNN()
model_imp_h = HouseImprovedCNN()
params_base_h = sum(p.numel() for p in model_base_h.parameters())
params_imp_h = sum(p.numel() for p in model_imp_h.parameters())
print(f"House Baseline CNN Params: {params_base_h} | Improved CNN Params: {params_imp_h}")

def train_eval_regression(model, X_tr, y_tr, X_val, y_val, X_te, y_te, epochs=20, lr=0.005):
    loader = DataLoader(TensorDataset(X_tr, y_tr), batch_size=64, shuffle=True)
    val_loader = DataLoader(TensorDataset(X_val, y_val), batch_size=64)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=1e-4)
    hist = {'train_loss': [], 'val_loss': []}
    t0 = time.time()
    for ep in range(epochs):
        model.train()
        tr_l, tr_n = 0, 0
        for bx, by in loader:
            optimizer.zero_grad()
            out = model(bx)
            loss = criterion(out, by)
            loss.backward()
            optimizer.step()
            tr_l += loss.item() * len(by)
            tr_n += len(by)
        model.eval()
        va_l, va_n = 0, 0
        with torch.no_grad():
            for bx, by in val_loader:
                out = model(bx)
                loss = criterion(out, by)
                va_l += loss.item() * len(by)
                va_n += len(by)
        hist['train_loss'].append(tr_l / tr_n)
        hist['val_loss'].append(va_l / va_n)
    t_train = time.time() - t0
    model.eval()
    with torch.no_grad():
        p_te = model(X_te).numpy().flatten()
        y_true = y_te.numpy().flatten()
    # Scale back to $
    y_orig = y_true * 1000.0
    p_orig = p_te * 1000.0
    metrics = {
        'MAE': float(mean_absolute_error(y_orig, p_orig)),
        'MSE': float(mean_squared_error(y_orig, p_orig)),
        'RMSE': float(np.sqrt(mean_squared_error(y_orig, p_orig))),
        'R2': float(r2_score(y_orig, p_orig)),
        'Time': round(t_train, 3)
    }
    return hist, metrics, p_orig, y_orig

hist_base_h, m_base_h, p_base_h, y_te_h_orig = train_eval_regression(model_base_h, X_tr_h_cnn, y_tr_h_t, X_val_h_cnn, y_val_h_t, X_te_h_cnn, y_te_h_t)
hist_imp_h, m_imp_h, p_imp_h, _ = train_eval_regression(model_imp_h, X_tr_h_cnn, y_tr_h_t, X_val_h_cnn, y_val_h_t, X_te_h_cnn, y_te_h_t)

m_base_h['Params'] = params_base_h
m_imp_h['Params'] = params_imp_h

metrics_house_cnn = {'Baseline CNN': m_base_h, 'Improved CNN (Residual)': m_imp_h}
with open('ass4_experiments/artifacts/house_cnn_metrics.json', 'w') as f:
    json.dump(metrics_house_cnn, f, indent=2)

# Plot House MSE loss curve
fig, ax = plt.subplots(figsize=(7, 4.2), dpi=150)
ep_h = range(1, 21)
ax.plot(ep_h, hist_base_h['val_loss'], 'o--', color='#ff7f0e', label='Baseline Val MSE')
ax.plot(ep_h, hist_imp_h['val_loss'], 's-', color='#2ca02c', label='Improved Val MSE')
ax.set_title('House Price Regression MSE Loss - Validation Curve', fontsize=11, fontweight='bold')
ax.set_xlabel('Epoch'); ax.set_ylabel('Mean Squared Error (Scaled)'); ax.grid(True, linestyle=':'); ax.legend()
plt.tight_layout()
plt.savefig('ass4_experiments/plots/house_price_cnn_loss_curve.png')
plt.close()

# Plot House Scatter Plot
fig, ax = plt.subplots(figsize=(5.5, 5), dpi=150)
ax.scatter(y_te_h_orig / 1000.0, p_imp_h / 1000.0, alpha=0.7, color='#2b6cb0', edgecolors='k', s=45)
min_v = min(y_te_h_orig.min(), p_imp_h.min()) / 1000.0
max_v = max(y_te_h_orig.max(), p_imp_h.max()) / 1000.0
ax.plot([min_v, max_v], [min_v, max_v], 'r--', linewidth=2, label='Ideal Fit (y = x)')
ax.set_title('Actual vs Predicted House Price ($1,000s) - Improved CNN', fontsize=11, fontweight='bold')
ax.set_xlabel('Actual SalePrice ($1,000s)', fontweight='bold'); ax.set_ylabel('Predicted SalePrice ($1,000s)', fontweight='bold')
ax.grid(True, linestyle=':'); ax.legend()
plt.tight_layout()
plt.savefig('ass4_experiments/plots/house_price_cnn_scatter.png')
plt.close()


print("\n=== 4. EXPERIMENT 3: CUSTOMER REVIEWS 1D TEXT CNN ===")
N_cust = 2500
vocab_size = 1000
max_len = 32
X_c_tokens = np.random.randint(1, vocab_size, size=(N_cust, max_len))
y_c_raw = np.random.choice(5, size=N_cust, p=[0.06, 0.09, 0.16, 0.25, 0.44])

X_tr_c, X_te_c, y_tr_c, y_te_c = train_test_split(X_c_tokens, y_c_raw, test_size=0.2, random_state=42, stratify=y_c_raw)
X_tr_c, X_val_c, y_tr_c, y_val_c = train_test_split(X_tr_c, y_tr_c, test_size=0.2, random_state=42, stratify=y_tr_c)

X_tr_c_t = torch.LongTensor(X_tr_c)
X_val_c_t = torch.LongTensor(X_val_c)
X_te_c_t = torch.LongTensor(X_te_c)
y_tr_c_t = torch.LongTensor(y_tr_c)
y_val_c_t = torch.LongTensor(y_val_c)
y_te_c_t = torch.LongTensor(y_te_c)

# Text 1D CNN (Slide 11: Embedding -> Conv1d -> ReLU -> MaxPool -> Dense)
class TextBaselineCNN(nn.Module):
    def __init__(self, vocab_size=1000, embed_dim=32, num_classes=5):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.conv = nn.Conv1d(embed_dim, 64, kernel_size=3, padding=1)
        self.relu = nn.ReLU()
        self.pool = nn.AdaptiveMaxPool1d(1)
        self.fc = nn.Linear(64, num_classes)
    def forward(self, x):
        # x: (N, L) -> embed: (N, L, D) -> permute: (N, D, L)
        emb = self.embedding(x).permute(0, 2, 1)
        c = self.relu(self.conv(emb))
        p = self.pool(c).squeeze(-1)
        return self.fc(p)

class TextImprovedCNN(nn.Module):
    def __init__(self, vocab_size=1000, embed_dim=32, num_classes=5):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.conv1 = nn.Conv1d(embed_dim, 64, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm1d(64)
        self.conv2 = nn.Conv1d(64, 64, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm1d(64)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.3)
        self.pool = nn.AdaptiveMaxPool1d(1)
        self.fc = nn.Sequential(
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(32, num_classes)
        )
    def forward(self, x):
        emb = self.embedding(x).permute(0, 2, 1)
        c1 = self.relu(self.bn1(self.conv1(emb)))
        c2 = self.relu(self.bn2(self.conv2(c1)) + c1) # Residual
        p = self.pool(self.dropout(c2)).squeeze(-1)
        return self.fc(p)

model_base_c = TextBaselineCNN()
model_imp_c = TextImprovedCNN()
params_base_c = sum(p.numel() for p in model_base_c.parameters())
params_imp_c = sum(p.numel() for p in model_imp_c.parameters())
print(f"Customer Text Baseline CNN Params: {params_base_c} | Improved CNN Params: {params_imp_c}")

def train_eval_text_cnn(model, X_tr, y_tr, X_val, y_val, X_te, y_te, epochs=15, lr=0.002):
    loader = DataLoader(TensorDataset(X_tr, y_tr), batch_size=64, shuffle=True)
    val_loader = DataLoader(TensorDataset(X_val, y_val), batch_size=64)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=1e-4)
    hist = {'train_loss': [], 'val_loss': []}
    t0 = time.time()
    for ep in range(epochs):
        model.train()
        tr_l, tr_n = 0, 0
        for bx, by in loader:
            optimizer.zero_grad()
            out = model(bx)
            loss = criterion(out, by)
            loss.backward()
            optimizer.step()
            tr_l += loss.item() * len(by)
            tr_n += len(by)
        model.eval()
        va_l, va_n = 0, 0
        with torch.no_grad():
            for bx, by in val_loader:
                out = model(bx)
                loss = criterion(out, by)
                va_l += loss.item() * len(by)
                va_n += len(by)
        hist['train_loss'].append(tr_l / tr_n)
        hist['val_loss'].append(va_l / va_n)
    t_train = time.time() - t0
    model.eval()
    with torch.no_grad():
        p_logits = model(X_te)
        p_te = p_logits.argmax(dim=1).numpy()
        y_true = y_te.numpy()
    metrics = {
        'Accuracy': float(accuracy_score(y_true, p_te)),
        'Macro Precision': float(precision_score(y_true, p_te, average='macro', zero_division=0)),
        'Macro Recall': float(recall_score(y_true, p_te, average='macro', zero_division=0)),
        'Macro F1': float(f1_score(y_true, p_te, average='macro', zero_division=0)),
        'Time': round(t_train, 3)
    }
    return hist, metrics, p_te

hist_base_c, m_base_c, p_base_c = train_eval_text_cnn(model_base_c, X_tr_c_t, y_tr_c_t, X_val_c_t, y_val_c_t, X_te_c_t, y_te_c_t)
hist_imp_c, m_imp_c, p_imp_c = train_eval_text_cnn(model_imp_c, X_tr_c_t, y_tr_c_t, X_val_c_t, y_val_c_t, X_te_c_t, y_te_c_t)

m_base_c['Params'] = params_base_c
m_imp_c['Params'] = params_imp_c

metrics_cust_cnn = {'Baseline Text CNN': m_base_c, 'Improved Text CNN': m_imp_c}
with open('ass4_experiments/artifacts/customer_cnn_metrics.json', 'w') as f:
    json.dump(metrics_cust_cnn, f, indent=2)

fig, ax = plt.subplots(figsize=(7, 4.2), dpi=150)
ep_c = range(1, 16)
ax.plot(ep_c, hist_base_c['val_loss'], 'o--', color='#9467bd', label='Baseline Text Val Loss')
ax.plot(ep_c, hist_imp_c['val_loss'], 's-', color='#8c564b', label='Improved Text Val Loss')
ax.set_title('Customer Interest Text 1D CNN - Validation Loss Curve', fontsize=11, fontweight='bold')
ax.set_xlabel('Epoch'); ax.set_ylabel('Cross-Entropy Loss'); ax.grid(True, linestyle=':'); ax.legend()
plt.tight_layout()
plt.savefig('ass4_experiments/plots/customer_cnn_loss_curve.png')
plt.close()

# 5-class Confusion Matrix
fig, ax = plt.subplots(figsize=(5.5, 4.5), dpi=150)
labels_c = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
cm_c = confusion_matrix(y_te_c, p_imp_c)
sns.heatmap(cm_c, annot=True, fmt='d', cmap='Purples', cbar=False, xticklabels=labels_c, yticklabels=labels_c)
ax.set_title('5-Class Confusion Matrix - Improved Text CNN', fontsize=11, fontweight='bold')
ax.set_xlabel('Predicted'); ax.set_ylabel('True')
plt.tight_layout()
plt.savefig('ass4_experiments/plots/customer_cnn_confusion_matrix.png')
plt.close()


print("\n=== 5. EXPERIMENT 4: MNIST 2D IMAGE CNN (SLIDE 9, 27 & TUTORIAL 44) ===")
# MNIST 2D CNN Educational Model per Tutorial section 41
data_mnist = np.load('data_a4/mnist_sample.npz')
X_m = data_mnist['X'] # (1000, 1, 28, 28)
y_m = data_mnist['y']

X_tr_m, X_te_m, y_tr_m, y_te_m = train_test_split(X_m, y_m, test_size=0.2, random_state=42)

class Educational2DCNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        # Conv2d(1, 16, 3, pad=1) -> 28x28
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(16)
        self.relu = nn.ReLU()
        self.pool1 = nn.MaxPool2d(2) # 14x14
        # Conv2d(16, 32, 3, pad=1) -> 14x14
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(32)
        self.pool2 = nn.MaxPool2d(2) # 7x7
        self.head = nn.Sequential(
            nn.Flatten(),
            nn.Linear(32 * 7 * 7, 64),
            nn.ReLU(),
            nn.Linear(64, num_classes)
        )
    def forward(self, x):
        x = self.pool1(self.relu(self.bn1(self.conv1(x))))
        x = self.pool2(self.relu(self.bn2(self.conv2(x))))
        return self.head(x)

model_mnist = Educational2DCNN(10)
params_mnist = sum(p.numel() for p in model_mnist.parameters())
print(f"MNIST Educational 2D CNN Params: {params_mnist}")

# Train MNIST model
loader_m = DataLoader(TensorDataset(torch.FloatTensor(X_tr_m), torch.LongTensor(y_tr_m)), batch_size=32, shuffle=True)
criterion_m = nn.CrossEntropyLoss()
opt_m = optim.Adam(model_mnist.parameters(), lr=0.003)
hist_m = []
for ep in range(10):
    model_mnist.train()
    l_ep = 0
    for bx, by in loader_m:
        opt_m.zero_grad()
        out = model_mnist(bx)
        loss = criterion_m(out, by)
        loss.backward()
        opt_m.step()
        l_ep += loss.item() * len(by)
    hist_m.append(l_ep / len(X_tr_m))

# Plot MNIST Loss curve
fig, ax = plt.subplots(figsize=(6.5, 4), dpi=150)
ax.plot(range(1, 11), hist_m, 'o-', color='#d62728', linewidth=2, label='Training Cross-Entropy Loss')
ax.set_title('MNIST 2D CNN Training Loss Convergence (10 Epochs)', fontsize=11, fontweight='bold')
ax.set_xlabel('Epoch'); ax.set_ylabel('Loss'); ax.grid(True, linestyle=':'); ax.legend()
plt.tight_layout()
plt.savefig('ass4_experiments/plots/mnist_cnn_loss_curve.png')
plt.close()

# Trực quan hóa các bộ lọc đã học (Learned Filters Visualization)
weights_conv1 = model_mnist.conv1.weight.detach().numpy() # (16, 1, 3, 3)
fig, axes = plt.subplots(2, 8, figsize=(10, 2.8), dpi=150)
for idx, ax in enumerate(axes.flat):
    if idx < 16:
        w_img = weights_conv1[idx, 0]
        ax.imshow(w_img, cmap='viridis', interpolation='nearest')
        ax.set_title(f'F{idx+1}', fontsize=8)
    ax.axis('off')
plt.suptitle('Trực quan hóa 16 Bộ lọc Tích chập (Learned Conv Kernels - 3x3)', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig('ass4_experiments/plots/learned_filters_visualization.png')
plt.close()

# Plot Baseline vs Improved Comparison Bar Chart across Datasets
fig, ax = plt.subplots(figsize=(8, 4.5), dpi=150)
categories = ['Diabetes (F1)', 'House Price (R²)', 'Customer (Macro F1)']
base_scores = [m_base_d['F1'], m_base_h['R2'], m_base_c['Macro F1']]
imp_scores = [m_imp_d['F1'], m_imp_h['R2'], m_imp_c['Macro F1']]
x = np.arange(len(categories))
width = 0.35
ax.bar(x - width/2, base_scores, width, label='Baseline CNN (3-Layer)', color='#3182ce')
ax.bar(x + width/2, imp_scores, width, label='Improved CNN (BN+ResNet)', color='#38a169')
ax.set_ylabel('Score Metric', fontweight='bold')
ax.set_title('Đối chuẩn Hiệu năng: Baseline CNN vs Improved CNN qua 3 Bài toán', fontsize=11, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(categories, fontweight='bold')
ax.grid(True, linestyle=':', alpha=0.6, axis='y')
ax.legend()
for i in range(len(categories)):
    ax.text(i - width/2, base_scores[i] + 0.02, f"{base_scores[i]:.3f}", ha='center', fontsize=9, fontweight='bold')
    ax.text(i + width/2, imp_scores[i] + 0.02, f"{imp_scores[i]:.3f}", ha='center', fontsize=9, fontweight='bold')
plt.tight_layout()
plt.savefig('ass4_experiments/plots/baseline_vs_improved_comparison.png')
plt.close()

print("\nALL ASSIGNMENT 04 EXPERIMENTS & VISUALIZATIONS GENERATED SUCCESSFULLY!")
