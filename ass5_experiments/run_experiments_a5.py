import os, sys, time, json, copy, random
sys.stdout.reconfigure(encoding='utf-8')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, random_split, TensorDataset
from torchvision import datasets, transforms
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# -------------------------------------------------------------
# 1. SETUP SEED VÀ THƯ MỤC
# -------------------------------------------------------------
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"[*] Thiết bị tính toán sử dụng: {device}")

os.makedirs('ass5_experiments/plots', exist_ok=True)
os.makedirs('ass5_experiments/artifacts', exist_ok=True)
os.makedirs('ass5_experiments/rendered_cells', exist_ok=True)
os.makedirs('ass5', exist_ok=True)

# -------------------------------------------------------------
# 2. ĐỊNH NGHĨA CÁC KIẾN TRÚC MÔ HÌNH (M1 - M7 cho 2D & M1 - M4 cho 1D)
# -------------------------------------------------------------

def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

# --- 2D IMAGE MODELS ---
class BasicCNN(nn.Module):
    def __init__(self, in_channels=1, num_classes=10):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, 16, 3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        self.fc = nn.Linear(32 * 7 * 7, num_classes)
    def forward(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), 2)
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        return self.fc(x.flatten(1))

class BatchNormCNN(nn.Module):
    def __init__(self, in_channels=1, num_classes=10):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, 16, 3, padding=1)
        self.bn1 = nn.BatchNorm2d(16)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        self.bn2 = nn.BatchNorm2d(32)
        self.fc = nn.Linear(32 * 7 * 7, num_classes)
    def forward(self, x):
        x = F.max_pool2d(F.relu(self.bn1(self.conv1(x))), 2)
        x = F.max_pool2d(F.relu(self.bn2(self.conv2(x))), 2)
        return self.fc(x.flatten(1))

class ResBlock2D(nn.Module):
    def __init__(self, c):
        super().__init__()
        self.conv1 = nn.Conv2d(c, c, 3, padding=1)
        self.bn1 = nn.BatchNorm2d(c)
        self.conv2 = nn.Conv2d(c, c, 3, padding=1)
        self.bn2 = nn.BatchNorm2d(c)
    def forward(self, x):
        return F.relu(x + self.bn2(self.conv2(F.relu(self.bn1(self.conv1(x))))))

class ResidualCNN(nn.Module):
    def __init__(self, in_channels=1, num_classes=10):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, 16, 3, padding=1)
        self.bn1 = nn.BatchNorm2d(16)
        self.res = ResBlock2D(16)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        self.bn2 = nn.BatchNorm2d(32)
        self.fc = nn.Linear(32 * 7 * 7, num_classes)
    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.max_pool2d(self.res(x), 2)
        x = F.max_pool2d(F.relu(self.bn2(self.conv2(x))), 2)
        return self.fc(x.flatten(1))

class SEBlock2D(nn.Module):
    def __init__(self, c, r=4):
        super().__init__()
        self.fc1 = nn.Linear(c, c // r)
        self.fc2 = nn.Linear(c // r, c)
    def forward(self, x):
        b, c, _, _ = x.shape
        w = F.adaptive_avg_pool2d(x, 1).view(b, c)
        w = torch.sigmoid(self.fc2(F.relu(self.fc1(w)))).view(b, c, 1, 1)
        return x * w

class AttentionCNN(nn.Module):
    def __init__(self, in_channels=1, num_classes=10):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, 16, 3, padding=1)
        self.bn1 = nn.BatchNorm2d(16)
        self.res = ResBlock2D(16)
        self.se = SEBlock2D(16, r=4)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        self.bn2 = nn.BatchNorm2d(32)
        self.fc = nn.Linear(32 * 7 * 7, num_classes)
    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.se(self.res(x))
        x = F.max_pool2d(x, 2)
        x = F.max_pool2d(F.relu(self.bn2(self.conv2(x))), 2)
        return self.fc(x.flatten(1))

class AdaptedLeNet(nn.Module):
    def __init__(self, in_channels=1, num_classes=10):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, 6, 5)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 4 * 4, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, num_classes)
    def forward(self, x):
        x = F.avg_pool2d(F.relu(self.conv1(x)), 2)
        x = F.avg_pool2d(F.relu(self.conv2(x)), 2)
        x = x.flatten(1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)

class AdaptedAlexNet(nn.Module):
    def __init__(self, in_channels=1, num_classes=10):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, 32, 3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, 3, padding=1)
        self.fc1 = nn.Linear(128 * 7 * 7, 256)
        self.fc2 = nn.Linear(256, num_classes)
    def forward(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), 2)
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = F.relu(self.conv3(x))
        x = x.flatten(1)
        x = F.dropout(F.relu(self.fc1(x)), 0.5, training=self.training)
        return self.fc2(x)

class AdaptedVGG(nn.Module):
    def __init__(self, in_channels=1, num_classes=10):
        super().__init__()
        self.conv1_1 = nn.Conv2d(in_channels, 32, 3, padding=1)
        self.conv1_2 = nn.Conv2d(32, 32, 3, padding=1)
        self.conv2_1 = nn.Conv2d(32, 64, 3, padding=1)
        self.conv2_2 = nn.Conv2d(64, 64, 3, padding=1)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, num_classes)
    def forward(self, x):
        x = F.relu(self.conv1_1(x))
        x = F.max_pool2d(F.relu(self.conv1_2(x)), 2)
        x = F.relu(self.conv2_1(x))
        x = F.max_pool2d(F.relu(self.conv2_2(x)), 2)
        x = x.flatten(1)
        x = F.dropout(F.relu(self.fc1(x)), 0.5, training=self.training)
        return self.fc2(x)

# --- 1D TABULAR MODELS FOR DIABETES ---
class DiabetesBasicCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv1d(1, 16, 3, padding=1)
        self.conv2 = nn.Conv1d(16, 32, 3, padding=1)
        self.fc = nn.Linear(32 * 4, 1)
    def forward(self, x):
        x = F.max_pool1d(F.relu(self.conv1(x)), 2)
        x = F.relu(self.conv2(x))
        return self.fc(x.flatten(1))

class DiabetesBatchNormCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv1d(1, 16, 3, padding=1)
        self.bn1 = nn.BatchNorm1d(16)
        self.conv2 = nn.Conv1d(16, 32, 3, padding=1)
        self.bn2 = nn.BatchNorm1d(32)
        self.fc = nn.Linear(32 * 4, 1)
    def forward(self, x):
        x = F.max_pool1d(F.relu(self.bn1(self.conv1(x))), 2)
        x = F.relu(self.bn2(self.conv2(x)))
        return self.fc(x.flatten(1))

class ResBlock1D(nn.Module):
    def __init__(self, c):
        super().__init__()
        self.conv1 = nn.Conv1d(c, c, 3, padding=1)
        self.bn1 = nn.BatchNorm1d(c)
        self.conv2 = nn.Conv1d(c, c, 3, padding=1)
        self.bn2 = nn.BatchNorm1d(c)
    def forward(self, x):
        return F.relu(x + self.bn2(self.conv2(F.relu(self.bn1(self.conv1(x))))))

class DiabetesResidualCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv1d(1, 16, 3, padding=1)
        self.bn1 = nn.BatchNorm1d(16)
        self.res = ResBlock1D(16)
        self.conv2 = nn.Conv1d(16, 32, 3, padding=1)
        self.bn2 = nn.BatchNorm1d(32)
        self.fc = nn.Linear(32 * 4, 1)
    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.max_pool1d(self.res(x), 2)
        x = F.relu(self.bn2(self.conv2(x)))
        return self.fc(x.flatten(1))

class SEBlock1D(nn.Module):
    def __init__(self, c, r=4):
        super().__init__()
        self.fc1 = nn.Linear(c, c // r)
        self.fc2 = nn.Linear(c // r, c)
    def forward(self, x):
        b, c, _ = x.shape
        w = F.adaptive_avg_pool1d(x, 1).view(b, c)
        w = torch.sigmoid(self.fc2(F.relu(self.fc1(w)))).view(b, c, 1)
        return x * w

class DiabetesAttentionCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv1d(1, 16, 3, padding=1)
        self.bn1 = nn.BatchNorm1d(16)
        self.res = ResBlock1D(16)
        self.se = SEBlock1D(16, r=4)
        self.conv2 = nn.Conv1d(16, 32, 3, padding=1)
        self.bn2 = nn.BatchNorm1d(32)
        self.fc = nn.Linear(32 * 4, 1)
    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.se(self.res(x))
        x = F.max_pool1d(x, 2)
        x = F.relu(self.bn2(self.conv2(x)))
        return self.fc(x.flatten(1))

print("[*] Đã khai báo thành công 7 kiến trúc 2D và 4 kiến trúc 1D.")

# -------------------------------------------------------------
# 3. CHUẨN BỊ DỮ LIỆU (MNIST, FASHION-MNIST, DIABETES)
# -------------------------------------------------------------
print("\n=== [CHUẨN BỊ DỮ LIỆU] ===")

# 3.1. MNIST
mnist_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])
mnist_train_full = datasets.MNIST(root='data', train=True, download=False, transform=mnist_transform)
mnist_test = datasets.MNIST(root='data', train=False, download=False, transform=mnist_transform)
mnist_train, mnist_val = random_split(mnist_train_full, [54000, 6000], generator=torch.Generator().manual_seed(SEED))

mnist_train_loader = DataLoader(mnist_train, batch_size=64, shuffle=True)
mnist_val_loader = DataLoader(mnist_val, batch_size=1000, shuffle=False)
mnist_test_loader = DataLoader(mnist_test, batch_size=1000, shuffle=False)
print(f"[OK] MNIST: {len(mnist_train)} train, {len(mnist_val)} val, {len(mnist_test)} test.")

# 3.2. Fashion-MNIST
fmnist_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.2860,), (0.3530,))
])
fmnist_train_full = datasets.FashionMNIST(root='data', train=True, download=False, transform=fmnist_transform)
fmnist_test = datasets.FashionMNIST(root='data', train=False, download=False, transform=fmnist_transform)
fmnist_train, fmnist_val = random_split(fmnist_train_full, [54000, 6000], generator=torch.Generator().manual_seed(SEED))

fmnist_train_loader = DataLoader(fmnist_train, batch_size=64, shuffle=True)
fmnist_val_loader = DataLoader(fmnist_val, batch_size=1000, shuffle=False)
fmnist_test_loader = DataLoader(fmnist_test, batch_size=1000, shuffle=False)
print(f"[OK] Fashion-MNIST: {len(fmnist_train)} train, {len(fmnist_val)} val, {len(fmnist_test)} test.")

# 3.3. Diabetes
df_diab = pd.read_csv('data/diabetes.csv')
zero_cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
for col in zero_cols:
    df_diab[col] = df_diab[col].replace(0, np.nan)
    df_diab[col] = df_diab[col].fillna(df_diab.groupby('Outcome')[col].transform('median'))

X = df_diab.drop('Outcome', axis=1).values
y = df_diab['Outcome'].values

# Split 70% train, 15% val, 15% test
X_train_d, X_temp_d, y_train_d, y_temp_d = train_test_split(X, y, test_size=0.30, random_state=SEED, stratify=y)
X_val_d, X_test_d, y_val_d, y_test_d = train_test_split(X_temp_d, y_temp_d, test_size=0.50, random_state=SEED, stratify=y_temp_d)

scaler = StandardScaler()
X_train_d = scaler.fit_transform(X_train_d)
X_val_d = scaler.transform(X_val_d)
X_test_d = scaler.transform(X_test_d)

train_tensor_d = TensorDataset(torch.tensor(X_train_d, dtype=torch.float32).unsqueeze(1), torch.tensor(y_train_d, dtype=torch.float32).unsqueeze(1))
val_tensor_d = TensorDataset(torch.tensor(X_val_d, dtype=torch.float32).unsqueeze(1), torch.tensor(y_val_d, dtype=torch.float32).unsqueeze(1))
test_tensor_d = TensorDataset(torch.tensor(X_test_d, dtype=torch.float32).unsqueeze(1), torch.tensor(y_test_d, dtype=torch.float32).unsqueeze(1))

diab_train_loader = DataLoader(train_tensor_d, batch_size=32, shuffle=True)
diab_val_loader = DataLoader(val_tensor_d, batch_size=len(val_tensor_d), shuffle=False)
diab_test_loader = DataLoader(test_tensor_d, batch_size=len(test_tensor_d), shuffle=False)
print(f"[OK] Diabetes: {len(X_train_d)} train, {len(X_val_d)} val, {len(X_test_d)} test.")

# -------------------------------------------------------------
# 4. HÀM HUẤN LUYỆN VÀ ĐÁNH GIÁ (CHỈ LƯU BEST STATE THEO VAL ACC)
# -------------------------------------------------------------

def train_image_model(model, train_loader, val_loader, epochs=5, lr=0.001):
    model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()
    
    best_val_acc = 0.0
    best_state = None
    history = {'train_loss': [], 'val_loss': [], 'train_acc': [], 'val_acc': []}
    
    t0 = time.time()
    for ep in range(1, epochs + 1):
        model.train()
        total_loss, correct, total = 0.0, 0, 0
        for x, y in train_loader:
            x, y = x.to(device), y.to(device)
            optimizer.zero_grad()
            out = model(x)
            loss = criterion(out, y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * len(y)
            pred = out.argmax(1)
            correct += pred.eq(y).sum().item()
            total += len(y)
            
        train_loss = total_loss / total
        train_acc = correct / total
        
        # Validation
        model.eval()
        v_loss, v_corr, v_tot = 0.0, 0, 0
        with torch.no_grad():
            for x, y in val_loader:
                x, y = x.to(device), y.to(device)
                out = model(x)
                loss = criterion(out, y)
                v_loss += loss.item() * len(y)
                pred = out.argmax(1)
                v_corr += pred.eq(y).sum().item()
                v_tot += len(y)
        val_loss = v_loss / v_tot
        val_acc = v_corr / v_tot
        
        history['train_loss'].append(train_loss)
        history['val_loss'].append(val_loss)
        history['train_acc'].append(train_acc)
        history['val_acc'].append(val_acc)
        
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_state = copy.deepcopy(model.state_dict())
            
    train_time = time.time() - t0
    model.load_state_dict(best_state)
    return model, history, train_time

def evaluate_image_model(model, test_loader):
    model.eval()
    criterion = nn.CrossEntropyLoss()
    total_loss, y_true, y_pred = 0.0, [], []
    with torch.no_grad():
        for x, y in test_loader:
            x, y = x.to(device), y.to(device)
            out = model(x)
            loss = criterion(out, y)
            total_loss += loss.item() * len(y)
            pred = out.argmax(1)
            y_true.extend(y.cpu().numpy())
            y_pred.extend(pred.cpu().numpy())
            
    test_loss = total_loss / len(y_true)
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, average='weighted', zero_division=0)
    rec = recall_score(y_true, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
    cm = confusion_matrix(y_true, y_pred)
    return test_loss, acc, prec, rec, f1, cm

def train_diabetes_model(model, train_loader, val_loader, epochs=15, lr=0.001):
    model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.BCEWithLogitsLoss()
    
    best_val_acc = 0.0
    best_state = None
    history = {'train_loss': [], 'val_loss': [], 'train_acc': [], 'val_acc': []}
    
    t0 = time.time()
    for ep in range(1, epochs + 1):
        model.train()
        total_loss, correct, total = 0.0, 0, 0
        for x, y in train_loader:
            x, y = x.to(device), y.to(device)
            optimizer.zero_grad()
            out = model(x)
            loss = criterion(out, y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * len(y)
            pred = (torch.sigmoid(out) >= 0.5).float()
            correct += pred.eq(y).sum().item()
            total += len(y)
            
        train_loss = total_loss / total
        train_acc = correct / total
        
        # Validation
        model.eval()
        v_loss, v_corr, v_tot = 0.0, 0, 0
        with torch.no_grad():
            for x, y in val_loader:
                x, y = x.to(device), y.to(device)
                out = model(x)
                loss = criterion(out, y)
                v_loss += loss.item() * len(y)
                pred = (torch.sigmoid(out) >= 0.5).float()
                v_corr += pred.eq(y).sum().item()
                v_tot += len(y)
        val_loss = v_loss / v_tot
        val_acc = v_corr / v_tot
        
        history['train_loss'].append(train_loss)
        history['val_loss'].append(val_loss)
        history['train_acc'].append(train_acc)
        history['val_acc'].append(val_acc)
        
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_state = copy.deepcopy(model.state_dict())
            
    train_time = time.time() - t0
    model.load_state_dict(best_state)
    return model, history, train_time

def evaluate_diabetes_model(model, test_loader):
    model.eval()
    criterion = nn.BCEWithLogitsLoss()
    total_loss, y_true, y_pred = 0.0, [], []
    with torch.no_grad():
        for x, y in test_loader:
            x, y = x.to(device), y.to(device)
            out = model(x)
            loss = criterion(out, y)
            total_loss += loss.item() * len(y)
            pred = (torch.sigmoid(out) >= 0.5).float()
            y_true.extend(y.cpu().numpy().flatten())
            y_pred.extend(pred.cpu().numpy().flatten())
            
    test_loss = total_loss / len(y_true)
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, average='weighted', zero_division=0)
    rec = recall_score(y_true, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
    cm = confusion_matrix(y_true, y_pred)
    return test_loss, acc, prec, rec, f1, cm

# -------------------------------------------------------------
# 5. TIẾN HÀNH CHẠY TOÀN BỘ 18 LƯỢT THỰC NGHIỆM
# -------------------------------------------------------------
metrics_results = {
    'MNIST': {},
    'Fashion-MNIST': {},
    'Diabetes': {}
}

# 5.1. Huấn luyện 7 mô hình trên MNIST
print("\n=== [THỰC NGHIỆM 1: MNIST - 7 MODELS] ===")
image_models_mnist = {
    'M1 Basic CNN': BasicCNN(),
    'M2 BatchNorm': BatchNormCNN(),
    'M3 Residual': ResidualCNN(),
    'M4 Attention': AttentionCNN(),
    'M5 LeNet': AdaptedLeNet(),
    'M6 Adapted AlexNet': AdaptedAlexNet(),
    'M7 Adapted VGG': AdaptedVGG()
}

for name, model in image_models_mnist.items():
    print(f"--> Đang huấn luyện {name} trên MNIST (5 Epochs)...")
    m, hist, t_sec = train_image_model(model, mnist_train_loader, mnist_val_loader, epochs=5)
    t_loss, acc, prec, rec, f1, cm = evaluate_image_model(m, mnist_test_loader)
    p_count = count_parameters(m)
    print(f"    [XONG] Params: {p_count:,} | Time: {t_sec:.2f}s | Test Loss: {t_loss:.6f} | Acc: {acc*100:.2f}%")
    metrics_results['MNIST'][name] = {
        'parameters': p_count,
        'time': t_sec,
        'test_loss': t_loss,
        'accuracy': acc,
        'precision': prec,
        'recall': rec,
        'f1': f1,
        'history': hist,
        'cm': cm.tolist()
    }

# 5.2. Huấn luyện 7 mô hình trên Fashion-MNIST
print("\n=== [THỰC NGHIỆM 2: FASHION-MNIST - 7 MODELS] ===")
image_models_fmnist = {
    'M1 Basic CNN': BasicCNN(),
    'M2 BatchNorm': BatchNormCNN(),
    'M3 Residual': ResidualCNN(),
    'M4 Attention': AttentionCNN(),
    'M5 LeNet': AdaptedLeNet(),
    'M6 Adapted AlexNet': AdaptedAlexNet(),
    'M7 Adapted VGG': AdaptedVGG()
}

for name, model in image_models_fmnist.items():
    print(f"--> Đang huấn luyện {name} trên Fashion-MNIST (5 Epochs)...")
    m, hist, t_sec = train_image_model(model, fmnist_train_loader, fmnist_val_loader, epochs=5)
    t_loss, acc, prec, rec, f1, cm = evaluate_image_model(m, fmnist_test_loader)
    p_count = count_parameters(m)
    print(f"    [XONG] Params: {p_count:,} | Time: {t_sec:.2f}s | Test Loss: {t_loss:.6f} | Acc: {acc*100:.2f}%")
    metrics_results['Fashion-MNIST'][name] = {
        'parameters': p_count,
        'time': t_sec,
        'test_loss': t_loss,
        'accuracy': acc,
        'precision': prec,
        'recall': rec,
        'f1': f1,
        'history': hist,
        'cm': cm.tolist()
    }

# 5.3. Huấn luyện 4 mô hình trên Diabetes
print("\n=== [THỰC NGHIỆM 3: DIABETES - 4 MODELS] ===")
diab_models = {
    'M1 Basic CNN': DiabetesBasicCNN(),
    'M2 BatchNorm': DiabetesBatchNormCNN(),
    'M3 Residual': DiabetesResidualCNN(),
    'M4 Attention': DiabetesAttentionCNN()
}

for name, model in diab_models.items():
    print(f"--> Đang huấn luyện {name} trên Diabetes (15 Epochs)...")
    m, hist, t_sec = train_diabetes_model(model, diab_train_loader, diab_val_loader, epochs=15)
    t_loss, acc, prec, rec, f1, cm = evaluate_diabetes_model(m, diab_test_loader)
    p_count = count_parameters(m)
    print(f"    [XONG] Params: {p_count:,} | Time: {t_sec:.2f}s | Test Loss: {t_loss:.6f} | Acc: {acc*100:.2f}%")
    metrics_results['Diabetes'][name] = {
        'parameters': p_count,
        'time': t_sec,
        'test_loss': t_loss,
        'accuracy': acc,
        'precision': prec,
        'recall': rec,
        'f1': f1,
        'history': hist,
        'cm': cm.tolist()
    }

# Lưu số liệu JSON
with open('ass5_experiments/artifacts/a05_metrics.json', 'w', encoding='utf-8') as f:
    json.dump(metrics_results, f, indent=4)
print("\n[OK] Đã lưu toàn bộ số liệu vào ass5_experiments/artifacts/a05_metrics.json")

# -------------------------------------------------------------
# 6. SINH TẤT CẢ CÁC BIỂU ĐỒ VÀ TRỰC QUAN HÓA KHOA HỌC
# -------------------------------------------------------------
print("\n=== [SINH BIỂU ĐỒ & SƠ ĐỒ KHOA HỌC] ===")
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

# Hình 1: Quy trình thực nghiệm tổng quát Assignment 05
fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=150)
ax.axis('off')
box_t = dict(boxstyle='round,pad=0.6', facecolor='#EBF8FF', edgecolor='#2B6CB0', lw=1.5)
box_d = dict(boxstyle='round,pad=0.5', facecolor='#F7FAFC', edgecolor='#CBD5E0', lw=1.2)
box_m = dict(boxstyle='round,pad=0.5', facecolor='#FEFCBF', edgecolor='#D69E2E', lw=1.2)
box_e = dict(boxstyle='round,pad=0.5', facecolor='#C6F6D5', edgecolor='#38A169', lw=1.2)

ax.text(0.5, 0.92, 'ASSIGNMENT 05: PHÁT TRIỂN CÁC KIẾN TRÚC MẠNG NƠ-RON TÍCH CHẬP (CNN)', ha='center', va='center', fontsize=11, fontweight='bold', bbox=box_t)

ax.text(0.18, 0.65, '1. BA TẬP DỮ LIỆU\n• MNIST (28×28 chữ số xám)\n• Fashion-MNIST (28×28 thời trang)\n• Diabetes (Bảng 8 đặc trưng 1D)', ha='center', va='center', fontsize=9, bbox=box_d)
ax.text(0.50, 0.65, '2. BẢY KIẾN TRÚC MÔ HÌNH\n• M1 Basic CNN | M2 BatchNorm\n• M3 Residual | M4 Attention SE\n• M5 LeNet | M6 AlexNet | M7 VGG', ha='center', va='center', fontsize=9, bbox=box_m)
ax.text(0.82, 0.65, '3. ĐÁNH GIÁ ĐỐI CHUẨN\n• Accuracy, Precision, Recall, F1\n• Training Time & Parameters\n• Ma trận nhầm lẫn 10 lớp & nhị phân', ha='center', va='center', fontsize=9, bbox=box_e)

ax.annotate('', xy=(0.34, 0.65), xytext=(0.30, 0.65), arrowprops=dict(arrowstyle='->', lw=1.5, color='#4A5568'))
ax.annotate('', xy=(0.66, 0.65), xytext=(0.62, 0.65), arrowprops=dict(arrowstyle='->', lw=1.5, color='#4A5568'))

ax.text(0.5, 0.25, 'QUY TRÌNH HUẤN LUYỆN:\nData Split (Train/Val/Test) ➔ PyTorch DataLoader ➔ Adam Optimizer (lr=0.001) ➔\nValidation Checkpointing (Best State Selection) ➔ Test Evaluation & Visualization', ha='center', va='center', fontsize=9, fontstyle='italic', bbox=dict(boxstyle='round,pad=0.5', facecolor='#EDF2F7', edgecolor='#718096', lw=1))

plt.tight_layout()
plt.savefig('ass5_experiments/plots/fig_01_overall_workflow.png')
plt.close()
print("[OK] Đã tạo Hình 1: fig_01_overall_workflow.png")

# Hình 2: Sơ đồ hàm hợp CNN
fig, ax = plt.subplots(figsize=(8.5, 3.2), dpi=150)
ax.axis('off')
blocks = [
    ('Input X\n(1×28×28)', '#EDF2F7'),
    ('Conv2D + Act\n$f_1(X) = \\sigma(W_1*X)$', '#BEE3F8'),
    ('Pooling\n$f_2(h_1) = MaxPool(h_1)$', '#E9D8FD'),
    ('Residual / SE\n$f_3(h_2) = \\mathcal{F}(h_2)+h_2$', '#FEFCBF'),
    ('Flatten + Dense\n$f_4(h_3) = W_L h_3 + b$', '#C6F6D5'),
    ('Logits $\\hat{y}$\n(10 classes)', '#FED7D7')
]
for idx, (b_text, col) in enumerate(blocks):
    x_pos = 0.08 + idx * 0.17
    ax.text(x_pos, 0.5, b_text, ha='center', va='center', fontsize=8.5, bbox=dict(boxstyle='round,pad=0.4', facecolor=col, edgecolor='#4A5568', lw=1.2))
    if idx < len(blocks) - 1:
        ax.annotate('', xy=(x_pos + 0.10, 0.5), xytext=(x_pos + 0.06, 0.5), arrowprops=dict(arrowstyle='->', lw=1.5, color='#2B6CB0'))

ax.text(0.5, 0.12, 'MÔ HÌNH HỌC SÂU DƯỚI DẠNG HÀM HỢP:   $\\hat{y} = (f_L \\circ \\dots \\circ f_2 \\circ f_1)(X)$', ha='center', va='center', fontsize=10, fontweight='bold', color='#1A365D')
plt.tight_layout()
plt.savefig('ass5_experiments/plots/fig_02_function_composition.png')
plt.close()
print("[OK] Đã tạo Hình 2: fig_02_function_composition.png")

# Hình 3: Mẫu ảnh MNIST
fig, axes = plt.subplots(1, 10, figsize=(10, 1.6), dpi=150)
for digit in range(10):
    for img, lbl in mnist_train_full:
        if lbl == digit:
            axes[digit].imshow(img.squeeze(), cmap='gray')
            axes[digit].set_title(f"Class: {digit}", fontsize=9)
            axes[digit].axis('off')
            break
plt.suptitle('Mẫu ảnh đại diện 10 chữ số tập dữ liệu MNIST (28×28)', fontsize=11, fontweight='bold', y=1.05)
plt.tight_layout()
plt.savefig('ass5_experiments/plots/fig_03_mnist_samples.png')
plt.close()
print("[OK] Đã tạo Hình 3: fig_03_mnist_samples.png")

# Hình 5: Mẫu ảnh Fashion-MNIST
fmnist_classes = ['T-shirt', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
fig, axes = plt.subplots(1, 10, figsize=(11, 1.8), dpi=150)
for cls_idx in range(10):
    for img, lbl in fmnist_train_full:
        if lbl == cls_idx:
            axes[cls_idx].imshow(img.squeeze(), cmap='gray')
            axes[cls_idx].set_title(f"{fmnist_classes[cls_idx]}", fontsize=8)
            axes[cls_idx].axis('off')
            break
plt.suptitle('Mẫu đại diện 10 lớp sản phẩm thời trang tập Fashion-MNIST (28×28)', fontsize=11, fontweight='bold', y=1.05)
plt.tight_layout()
plt.savefig('ass5_experiments/plots/fig_05_fashion_mnist_samples.png')
plt.close()
print("[OK] Đã tạo Hình 5: fig_05_fashion_mnist_samples.png")

# Hình 7: Phân bố nhãn Diabetes
fig, ax = plt.subplots(figsize=(5, 3.5), dpi=150)
sns.countplot(x='Outcome', data=df_diab, ax=ax, palette=['#3182CE', '#E53E3E'])
ax.set_title('Phân bố 2 lớp biến mục tiêu Outcome trong tập Diabetes', fontsize=10, fontweight='bold')
ax.set_xlabel('Outcome (0: Không tiểu đường | 1: Mắc tiểu đường)', fontsize=9)
ax.set_ylabel('Số lượng mẫu', fontsize=9)
for p in ax.patches:
    ax.annotate(f"{int(p.get_height())} mẫu ({p.get_height()/len(df_diab)*100:.1f}%)", (p.get_x() + 0.15, p.get_height() + 10), fontsize=8.5)
plt.tight_layout()
plt.savefig('ass5_experiments/plots/fig_07_diabetes_outcome_distribution.png')
plt.close()
print("[OK] Đã tạo Hình 7: fig_07_diabetes_outcome_distribution.png")

# Hình 23: Loss curves MNIST (7 models)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2), dpi=150)
colors = ['#3182CE', '#38A169', '#E53E3E', '#805AD5', '#DD6B20', '#319795', '#D69E2E']
for idx, (m_name, m_data) in enumerate(metrics_results['MNIST'].items()):
    ax1.plot(range(1, 6), m_data['history']['train_loss'], label=m_name, color=colors[idx], marker='o', markersize=4)
    ax2.plot(range(1, 6), m_data['history']['val_loss'], label=m_name, color=colors[idx], marker='s', markersize=4)
ax1.set_title('Training Loss trên MNIST (5 Epochs)', fontsize=10, fontweight='bold')
ax1.set_xlabel('Epoch'); ax1.set_ylabel('Cross-Entropy Loss'); ax1.grid(True, linestyle='--', alpha=0.5); ax1.legend(fontsize=7.5)
ax2.set_title('Validation Loss trên MNIST (5 Epochs)', fontsize=10, fontweight='bold')
ax2.set_xlabel('Epoch'); ax2.set_ylabel('Cross-Entropy Loss'); ax2.grid(True, linestyle='--', alpha=0.5); ax2.legend(fontsize=7.5)
plt.tight_layout()
plt.savefig('ass5_experiments/plots/fig_23_mnist_loss_curves.png')
plt.close()
print("[OK] Đã tạo Hình 23: fig_23_mnist_loss_curves.png")

# Hình 24: Loss curves Fashion-MNIST (7 models)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2), dpi=150)
for idx, (m_name, m_data) in enumerate(metrics_results['Fashion-MNIST'].items()):
    ax1.plot(range(1, 6), m_data['history']['train_loss'], label=m_name, color=colors[idx], marker='o', markersize=4)
    ax2.plot(range(1, 6), m_data['history']['val_loss'], label=m_name, color=colors[idx], marker='s', markersize=4)
ax1.set_title('Training Loss trên Fashion-MNIST (5 Epochs)', fontsize=10, fontweight='bold')
ax1.set_xlabel('Epoch'); ax1.set_ylabel('Cross-Entropy Loss'); ax1.grid(True, linestyle='--', alpha=0.5); ax1.legend(fontsize=7.5)
ax2.set_title('Validation Loss trên Fashion-MNIST (5 Epochs)', fontsize=10, fontweight='bold')
ax2.set_xlabel('Epoch'); ax2.set_ylabel('Cross-Entropy Loss'); ax2.grid(True, linestyle='--', alpha=0.5); ax2.legend(fontsize=7.5)
plt.tight_layout()
plt.savefig('ass5_experiments/plots/fig_24_fashion_mnist_loss_curves.png')
plt.close()
print("[OK] Đã tạo Hình 24: fig_24_fashion_mnist_loss_curves.png")

# Hình 25: Loss curves Diabetes (4 models)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2), dpi=150)
colors_4 = ['#3182CE', '#38A169', '#E53E3E', '#805AD5']
for idx, (m_name, m_data) in enumerate(metrics_results['Diabetes'].items()):
    ax1.plot(range(1, 16), m_data['history']['train_loss'], label=m_name, color=colors_4[idx], marker='o', markersize=3)
    ax2.plot(range(1, 16), m_data['history']['val_loss'], label=m_name, color=colors_4[idx], marker='s', markersize=3)
ax1.set_title('Training Loss trên Diabetes (15 Epochs)', fontsize=10, fontweight='bold')
ax1.set_xlabel('Epoch'); ax1.set_ylabel('BCE With Logits Loss'); ax1.grid(True, linestyle='--', alpha=0.5); ax1.legend(fontsize=8)
ax2.set_title('Validation Loss trên Diabetes (15 Epochs)', fontsize=10, fontweight='bold')
ax2.set_xlabel('Epoch'); ax2.set_ylabel('BCE With Logits Loss'); ax2.grid(True, linestyle='--', alpha=0.5); ax2.legend(fontsize=8)
plt.tight_layout()
plt.savefig('ass5_experiments/plots/fig_25_diabetes_loss_curves.png')
plt.close()
print("[OK] Đã tạo Hình 25: fig_25_diabetes_loss_curves.png")

# Hình 26: Test Accuracy MNIST (7 models)
fig, ax = plt.subplots(figsize=(8.5, 4.0), dpi=150)
names_mnist = list(metrics_results['MNIST'].keys())
accs_mnist = [metrics_results['MNIST'][k]['accuracy'] * 100 for k in names_mnist]
bars = ax.bar(names_mnist, accs_mnist, color='#2B6CB0', edgecolor='#1A365D', width=0.55)
ax.set_title('So sánh Test Accuracy (%) của 7 mô hình trên tập MNIST', fontsize=11, fontweight='bold')
ax.set_ylabel('Accuracy (%)', fontsize=9.5)
ax.set_ylim(97.5, 100)
plt.xticks(rotation=20, ha='right', fontsize=8.5)
ax.grid(axis='y', linestyle='--', alpha=0.6)
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.08, f"{yval:.2f}%", ha='center', va='bottom', fontsize=8, fontweight='bold')
plt.tight_layout()
plt.savefig('ass5_experiments/plots/fig_26_mnist_test_accuracy.png')
plt.close()
print("[OK] Đã tạo Hình 26: fig_26_mnist_test_accuracy.png")

# Hình 27: Test Accuracy Fashion-MNIST (7 models)
fig, ax = plt.subplots(figsize=(8.5, 4.0), dpi=150)
names_fmnist = list(metrics_results['Fashion-MNIST'].keys())
accs_fmnist = [metrics_results['Fashion-MNIST'][k]['accuracy'] * 100 for k in names_fmnist]
bars = ax.bar(names_fmnist, accs_fmnist, color='#D69E2E', edgecolor='#744210', width=0.55)
ax.set_title('So sánh Test Accuracy (%) của 7 mô hình trên tập Fashion-MNIST', fontsize=11, fontweight='bold')
ax.set_ylabel('Accuracy (%)', fontsize=9.5)
ax.set_ylim(84.0, 93.0)
plt.xticks(rotation=20, ha='right', fontsize=8.5)
ax.grid(axis='y', linestyle='--', alpha=0.6)
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.15, f"{yval:.2f}%", ha='center', va='bottom', fontsize=8, fontweight='bold')
plt.tight_layout()
plt.savefig('ass5_experiments/plots/fig_27_fashion_mnist_test_accuracy.png')
plt.close()
print("[OK] Đã tạo Hình 27: fig_27_fashion_mnist_test_accuracy.png")

# Hình 28: Test Accuracy Diabetes (4 models)
fig, ax = plt.subplots(figsize=(6.5, 4.0), dpi=150)
names_diab = list(metrics_results['Diabetes'].keys())
accs_diab = [metrics_results['Diabetes'][k]['accuracy'] * 100 for k in names_diab]
bars = ax.bar(names_diab, accs_diab, color='#38A169', edgecolor='#22543D', width=0.50)
ax.set_title('So sánh Test Accuracy (%) của 4 mô hình Conv1D trên Diabetes', fontsize=11, fontweight='bold')
ax.set_ylabel('Accuracy (%)', fontsize=9.5)
ax.set_ylim(70.0, 92.0)
plt.xticks(rotation=15, ha='right', fontsize=8.5)
ax.grid(axis='y', linestyle='--', alpha=0.6)
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.35, f"{yval:.2f}%", ha='center', va='bottom', fontsize=8.5, fontweight='bold')
plt.tight_layout()
plt.savefig('ass5_experiments/plots/fig_28_diabetes_test_accuracy.png')
plt.close()
print("[OK] Đã tạo Hình 28: fig_28_diabetes_test_accuracy.png")

# Hình 29: So sánh thời gian huấn luyện MNIST & Fashion-MNIST
fig, ax = plt.subplots(figsize=(9, 4.2), dpi=150)
x_idx = np.arange(len(names_mnist))
width = 0.35
time_mnist = [metrics_results['MNIST'][k]['time'] for k in names_mnist]
time_fmnist = [metrics_results['Fashion-MNIST'][k]['time'] for k in names_mnist]

b1 = ax.bar(x_idx - width/2, time_mnist, width, label='MNIST (5 Epochs)', color='#3182CE', edgecolor='#1A365D')
b2 = ax.bar(x_idx + width/2, time_fmnist, width, label='Fashion-MNIST (5 Epochs)', color='#ED8936', edgecolor='#7B341E')
ax.set_title('So sánh thời gian huấn luyện (giây) của các mô hình trên MNIST & Fashion-MNIST', fontsize=11, fontweight='bold')
ax.set_ylabel('Thời gian (giây)', fontsize=9.5)
ax.set_xticks(x_idx)
ax.set_xticklabels(names_mnist, rotation=20, ha='right', fontsize=8.5)
ax.legend(fontsize=9)
ax.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('ass5_experiments/plots/fig_29_training_time_comparison.png')
plt.close()
print("[OK] Đã tạo Hình 29: fig_29_training_time_comparison.png")

# Hình 30: So sánh tham số trainable
fig, ax = plt.subplots(figsize=(8.5, 4.0), dpi=150)
params_list = [metrics_results['MNIST'][k]['parameters'] for k in names_mnist]
bars = ax.bar(names_mnist, params_list, color='#805AD5', edgecolor='#44337A', width=0.55)
ax.set_title('So sánh số tham số học được (Trainable Parameters) của 7 mô hình ảnh', fontsize=11, fontweight='bold')
ax.set_ylabel('Số lượng tham số (Thang đo Log)', fontsize=9.5)
ax.set_yscale('log')
plt.xticks(rotation=20, ha='right', fontsize=8.5)
ax.grid(axis='y', linestyle='--', alpha=0.6)
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval * 1.15, f"{yval:,}", ha='center', va='bottom', fontsize=7.5, fontweight='bold')
plt.tight_layout()
plt.savefig('ass5_experiments/plots/fig_30_trainable_parameters.png')
plt.close()
print("[OK] Đã tạo Hình 30: fig_30_trainable_parameters.png")

# Hình 31: Confusion Matrix M7 VGG trên MNIST
cm_vgg = np.array(metrics_results['MNIST']['M7 Adapted VGG']['cm'])
fig, ax = plt.subplots(figsize=(6, 5), dpi=150)
sns.heatmap(cm_vgg, annot=True, fmt='d', cmap='Blues', cbar=False, ax=ax, annot_kws={"size": 8.5})
ax.set_title('Ma trận nhầm lẫn của M7 Adapted VGG trên tập kiểm thử MNIST', fontsize=10, fontweight='bold')
ax.set_xlabel('Dự đoán (Predicted label)', fontsize=9)
ax.set_ylabel('Thực tế (True label)', fontsize=9)
plt.tight_layout()
plt.savefig('ass5_experiments/plots/fig_31_mnist_vgg_confusion_matrix.png')
plt.close()
print("[OK] Đã tạo Hình 31: fig_31_mnist_vgg_confusion_matrix.png")

# Hình 32: Confusion Matrix M6 AlexNet trên Fashion-MNIST
cm_alex = np.array(metrics_results['Fashion-MNIST']['M6 Adapted AlexNet']['cm'])
fig, ax = plt.subplots(figsize=(6.5, 5.5), dpi=150)
sns.heatmap(cm_alex, annot=True, fmt='d', cmap='Oranges', cbar=False, ax=ax,
            xticklabels=fmnist_classes, yticklabels=fmnist_classes, annot_kws={"size": 8})
ax.set_title('Ma trận nhầm lẫn của M6 Adapted AlexNet trên Fashion-MNIST', fontsize=10, fontweight='bold')
ax.set_xlabel('Dự đoán (Predicted label)', fontsize=9)
ax.set_ylabel('Thực tế (True label)', fontsize=9)
plt.xticks(rotation=30, ha='right', fontsize=8)
plt.yticks(rotation=0, fontsize=8)
plt.tight_layout()
plt.savefig('ass5_experiments/plots/fig_32_fashion_alexnet_confusion_matrix.png')
plt.close()
print("[OK] Đã tạo Hình 32: fig_32_fashion_alexnet_confusion_matrix.png")

# Hình 33: Confusion Matrix M3 Residual trên Diabetes
cm_diab = np.array(metrics_results['Diabetes']['M3 Residual']['cm'])
fig, ax = plt.subplots(figsize=(4.5, 3.8), dpi=150)
sns.heatmap(cm_diab, annot=True, fmt='d', cmap='Greens', cbar=False, ax=ax,
            xticklabels=['Non-Diabetic (0)', 'Diabetic (1)'], yticklabels=['Non-Diabetic (0)', 'Diabetic (1)'], annot_kws={"size": 10})
ax.set_title('Ma trận nhầm lẫn của M3 Residual trên tập Diabetes', fontsize=9.5, fontweight='bold')
ax.set_xlabel('Dự đoán (Predicted)', fontsize=9)
ax.set_ylabel('Thực tế (Actual)', fontsize=9)
plt.tight_layout()
plt.savefig('ass5_experiments/plots/fig_33_diabetes_residual_confusion_matrix.png')
plt.close()
print("[OK] Đã tạo Hình 33: fig_33_diabetes_residual_confusion_matrix.png")

print("\n=== HOÀN TẤT THỰC NGHIỆM HUẤN LUYỆN VÀ TẠO CÁC BIỂU ĐỒ A05! ===")
