<template>
  <div class="container mt-4">
    <h1 class="text-center mb-4">Admin Panel</h1>
    <div class="row">
      <div class="col-md-4 mb-3">
        <div class="card shadow-sm">
          <div class="card-body text-center">
            <i class="bi bi-database-fill text-primary" style="font-size: 3rem;"></i>
            <h5 class="card-title mt-3">Manage Data</h5>
            <p class="card-text">View, edit, and delete forest monitoring data.</p>
            <button class="btn btn-primary" @click="toggleManageData">Manage Data</button>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-3">
        <div class="card shadow-sm">
          <div class="card-body text-center">
            <i class="bi bi-upload text-success" style="font-size: 3rem;"></i>
            <h5 class="card-title mt-3">Import Data</h5>
            <p class="card-text">Bulk import data from Excel files.</p>
            <button class="btn btn-success" @click="openImportModal">Coming Soon</button>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-3">
        <div class="card shadow-sm">
          <div class="card-body text-center">
            <i class="bi bi-bar-chart-line text-info" style="font-size: 3rem;"></i>
            <h5 class="card-title mt-3">Analytics</h5>
            <p class="card-text">View detailed analytics and reports.</p>
            <router-link to="/" class="btn btn-info">View Charts</router-link>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-md-4 mb-3">
        <div class="card shadow-sm">
          <div class="card-body text-center">
            <i class="bi bi-people-fill text-warning" style="font-size: 3rem;"></i>
            <h5 class="card-title mt-3">User Management</h5>
            <p class="card-text">Manage users and permissions.</p>
            <button class="btn btn-warning" @click="toggleUserManagement">Manage Users</button>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-3">
        <div class="card shadow-sm">
          <div class="card-body text-center">
            <i class="bi bi-gear-fill text-secondary" style="font-size: 3rem;"></i>
            <h5 class="card-title mt-3">Settings</h5>
            <p class="card-text">Configure application settings.</p>
            <button class="btn btn-secondary" disabled>Coming Soon</button>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-3">
        <div class="card shadow-sm">
          <div class="card-body text-center">
            <i class="bi bi-shield-check text-danger" style="font-size: 3rem;"></i>
            <h5 class="card-title mt-3">Security</h5>
            <p class="card-text">Security settings and logs.</p>
            <button class="btn btn-danger" disabled>Coming Soon</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Manage Data Table -->
    <div v-if="showTable" class="mt-4">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h2>Forest Monitoring Data</h2>
        <button class="btn btn-success" @click="openCreateModal">Add New Data</button>
      </div>
      
      <!-- Filter Section -->
      <div class="card mb-3">
        <div class="card-body">
          <h5 class="card-title">Filter Data</h5>
          <div class="row">
            <div class="col-md-4 mb-3">
              <label class="form-label">Filter berdasarkan Negara</label>
              <input v-model="filterCountry" type="text" class="form-control" placeholder="Masukkan nama negara">
            </div>
            <div class="col-md-4 mb-3">
              <label class="form-label">Filter berdasarkan Driver</label>
              <input v-model="filterDriver" type="text" class="form-control" placeholder="Masukkan driver">
            </div>
            <div class="col-md-4 mb-3">
              <label class="form-label">Filter berdasarkan Tahun</label>
              <input v-model.number="filterYear" type="number" class="form-control" placeholder="Masukkan tahun">
            </div>
          </div>
          <button @click="clearFilters" class="btn btn-outline-secondary">Clear Filter</button>
        </div>
      </div>
      
      <div class="table-responsive">
        <table class="table table-striped table-bordered">
          <thead class="table-dark">
            <tr>
              <th>Country</th>
              <th>Driver</th>
              <th>Year</th>
              <th>TC Loss (ha)</th>
              <th>Threshold</th>
              <!-- <th>SDG Indicator</th> -->
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="entry in cases" :key="`${entry.country}-${entry.driver}-${entry.year}`">
              <td>{{ entry.country }}</td>
              <td>{{ entry.driver }}</td>
              <td>{{ entry.year }}</td>
              <td>{{ entry.tc_loss_ha }}</td>
              <td>{{ entry.threshold }}</td>
              <!-- <td>{{ entry.sdg_indicator }}</td> -->
              <td>
                <button class="btn btn-sm btn-warning me-2" @click="editCase(entry)">Edit</button>
                <button class="btn btn-sm btn-danger" @click="deleteCase(entry)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <!-- Pagination -->
      <div class="d-flex justify-content-between align-items-center mt-3">
        <div>
          Showing {{ (currentPage - 1) * limit + 1 }} to {{ Math.min(currentPage * limit, totalItems) }} of {{ totalItems }} entries
        </div>
        <nav>
          <ul class="pagination">
            <li class="page-item" :class="{ disabled: currentPage === 1 }">
              <a class="page-link" href="#" @click.prevent="prevPage">Previous</a>
            </li>
            <li v-for="page in visiblePages" :key="page" class="page-item" :class="{ active: page === currentPage }">
              <a class="page-link" href="#" @click.prevent="goToPage(page)">{{ page }}</a>
            </li>
            <li class="page-item" :class="{ disabled: currentPage === totalPages }">
              <a class="page-link" href="#" @click.prevent="nextPage">Next</a>
            </li>
          </ul>
        </nav>
      </div>
      <button class="btn btn-secondary mt-3" @click="showTable = false">Close Table</button>
    </div>

    <!-- User Management Table -->
    <div v-if="showUserTable" class="mt-4">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h2>User Management</h2>
      </div>
      
      <div class="table-responsive">
        <table class="table table-striped table-bordered">
          <thead class="table-dark">
            <tr>
              <th>Username</th>
              <th>Email</th>
              <th>Role</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id || user._id">
              <td>{{ user.username }}</td>
              <td>{{ user.email }}</td>
              <td><span :class="user.role === 'admin' ? 'badge bg-danger' : 'badge bg-primary'">{{ user.role }}</span></td>
              <td>
                <button v-if="user.role !== 'admin'" class="btn btn-sm btn-outline-danger me-2" @click="updateUserRole(user, 'admin')">Make Admin</button>
                <button v-if="user.role !== 'user'" class="btn btn-sm btn-outline-primary" @click="updateUserRole(user, 'user')">Make User</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <button class="btn btn-secondary mt-3" @click="showUserTable = false">Close Table</button>
    </div>

    <!-- Create Modal -->
    <div class="modal-backdrop" v-if="showCreateModal">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content shadow-lg border-0">
          <div class="modal-header bg-success text-white">
            <h5 class="modal-title"><i class="bi bi-plus-circle me-2"></i>Add New Data</h5>
            <button type="button" class="btn-close btn-close-white" @click="showCreateModal = false"></button>
          </div>
          <div class="modal-body p-4">
            <form @submit.prevent="createData">
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label text-muted small">Country</label>
                  <input v-model="createForm.country" type="text" class="form-control" required placeholder="e.g. Indonesia">
                </div>
                <div class="col-md-6">
                  <label class="form-label text-muted small">Year</label>
                  <input v-model.number="createForm.year" type="number" class="form-control" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label text-muted small">Driver</label>
                  <input v-model="createForm.driver" type="text" class="form-control" required placeholder="e.g. Mining">
                </div>
                <div class="col-md-6">
                  <label class="form-label text-muted small">Threshold</label>
                  <div class="input-group">
                    <input v-model.number="createForm.threshold" type="number" class="form-control" placeholder="30">
                    <span class="input-group-text">%</span>
                  </div>
                </div>
                <div class="col-12">
                  <label class="form-label fw-bold text-success">TC Loss (ha)</label>
                  <div class="input-group">
                    <input v-model.number="createForm.tc_loss_ha" type="number" step="any" class="form-control border-success" required>
                    <span class="input-group-text bg-success text-white">ha</span>
                  </div>
                </div>
              </div>
              <div class="d-flex justify-content-end mt-4 pt-3 border-top">
                <button type="button" class="btn btn-light me-2" @click="showCreateModal = false">Cancel</button>
                <button type="submit" class="btn btn-success px-4">Save Data</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <div class="modal-backdrop" v-if="showEditModal">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content shadow-lg border-0">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title"><i class="bi bi-pencil-square me-2"></i>Edit Data</h5>
            <button type="button" class="btn-close btn-close-white" @click="showEditModal = false"></button>
          </div>
          <div class="modal-body p-4">
            <form @submit.prevent="updateData">
              <div class="row g-3">
                <div class="col-12">
                  <div class="alert alert-light border-start border-primary border-4 py-2 mb-2">
                    <small class="text-muted">Editing record for:</small><br>
                    <strong>{{ editForm.country }} ({{ editForm.year }})</strong>
                  </div>
                </div>
                <div class="col-md-6">
                  <label class="form-label text-muted small">Country</label>
                  <input v-model="editForm.country" type="text" class="form-control">
                </div>
                <div class="col-md-6">
                  <label class="form-label text-muted small">Year</label>
                  <input v-model.number="editForm.year" type="number" class="form-control">
                </div>
                <div class="col-md-6">
                  <label class="form-label text-muted small">Driver</label>
                  <input v-model="editForm.driver" type="text" class="form-control">
                </div>
                <div class="col-md-6">
                  <label class="form-label text-muted small">Threshold</label>
                  <div class="input-group">
                    <input v-model.number="editForm.threshold" type="number" class="form-control">
                    <span class="input-group-text">%</span>
                  </div>
                </div>
                <div class="col-12">
                  <label class="form-label fw-bold text-primary">TC Loss (ha)</label>
                  <div class="input-group">
                    <input v-model.number="editForm.tc_loss_ha" type="number" step="any" class="form-control border-primary" required>
                    <span class="input-group-text bg-primary text-white">ha</span>
                  </div>
                </div>
              </div>
              <div class="d-flex justify-content-end mt-4 pt-3 border-top">
                <button type="button" class="btn btn-light me-2" @click="showEditModal = false">Cancel</button>
                <button type="submit" class="btn btn-primary px-4">Update Changes</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Import Modal -->
    <div class="modal-backdrop" v-if="showImportModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Import Data from Excel</h5>
            <button type="button" class="btn-close" @click="closeImportModal"></button>
          </div>
          <div class="modal-body">
            <p>Upload an Excel file to bulk import forest monitoring data.</p>
            <input type="file" class="form-control" accept=".xlsx,.xls" @change="handleFileUpload">
            <small class="text-muted">Supported formats: .xlsx, .xls</small>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeImportModal">Cancel</button>
            <button type="button" class="btn btn-primary" @click="importData" :disabled="!selectedFile">Import</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, reactive } from 'vue';

const showImportModal = ref(false);
const showCreateModal = ref(false);
const showEditModal = ref(false);
const selectedFile = ref(null);
const showTable = ref(false);
const showUserTable = ref(false);
const users = ref([]);
const cases = ref([]);
const currentPage = ref(1);
const totalPages = ref(1);
const totalItems = ref(0);
const limit = 15;

const createForm = reactive({
    country: '',
    driver: '',
    year: new Date().getFullYear(),
    tc_loss_ha: 0,
    threshold: 30
});

const editForm = reactive({
    id: null,
    originalCountry: '',
    originalDriver: '',
    originalYear: 0,
    country: '',
    driver: '',
    year: 0,
    tc_loss_ha: 0,
    threshold: 0
});

// Filters
const filterCountry = ref('');
const filterDriver = ref('');
const filterYear = ref(null);

// Watch filters and refetch data
watch([filterCountry, filterDriver, filterYear], () => {
  currentPage.value = 1; // Reset to first page
    fetchCases(1);
});

const visiblePages = computed(() => {
    const pages = [];
    const start = Math.max(1, currentPage.value - 2);
    const end = Math.min(totalPages.value, currentPage.value + 2);
    for (let i = start; i <= end; i++) {
        pages.push(i);
    }
    return pages;
});

const openCreateModal = () => {
    createForm.country = '';
    createForm.driver = '';
    createForm.year = new Date().getFullYear();
    createForm.tc_loss_ha = 0;
    createForm.threshold = 30;
    showCreateModal.value = true;
};

const openImportModal = () => {
    showImportModal.value = true;
};

const closeImportModal = () => {
    showImportModal.value = false;
    selectedFile.value = null;
};

const handleFileUpload = (event) => {
    selectedFile.value = event.target.files[0];
};

const importData = () => {
    if (selectedFile.value) {
        // Here you would implement the file upload logic
        alert(`Importing ${selectedFile.value.name}... (Feature not implemented yet)`);
        closeImportModal();
    }
};

const toggleManageData = async () => {
  if (!showTable.value) {
    await fetchCases(1);
  }
  showTable.value = !showTable.value;
  if (showTable.value) showUserTable.value = false;
};

const toggleUserManagement = async () => {
  if (!showUserTable.value) {
    try {
      const response = await fetch('/api/user/users');
      if (response.ok) {
        const result = await response.json();
        console.log('Debug Users Data:', result); // Cek console browser (F12) untuk melihat apakah ada field id/_id
        
        // Normalisasi data user: Pastikan setiap user memiliki properti 'id'
        const rawUsers = Array.isArray(result) ? result : (result.data || []);
        users.value = rawUsers.map(u => {
          // Cari ID dari berbagai kemungkinan field (id, _id, user_id, userId)
          let uid = u.id || u._id || u.user_id || u.userId;
          
          // Handle format MongoDB Extended JSON { "$oid": "..." } jika uid berupa object
          if (typeof uid === 'object' && uid && uid.$oid) uid = uid.$oid;
          if (!uid && u._id && typeof u._id === 'object' && u._id.$oid) uid = u._id.$oid;
          
          // Jika masih tidak ditemukan, coba cari key apapun yang mengandung kata 'id'
          if (!uid) {
             const key = Object.keys(u).find(k => k.toLowerCase().includes('id') && (typeof u[k] === 'string' || typeof u[k] === 'number'));
             if (key) uid = u[key];
          }

          if (!uid) console.warn('Warning: User missing ID from backend. Available keys:', Object.keys(u));
          return { ...u, id: uid };
        });
      }
    } catch (error) {
      console.error('Error fetching users:', error);
      alert('Gagal mengambil data user');
    }
  }
  showUserTable.value = !showUserTable.value;
  if (showUserTable.value) showTable.value = false;
};

const updateUserRole = async (user, newRole) => {
  if (!confirm(`Are you sure you want to change ${user.username}'s role to ${newRole}?`)) return;

  try {
    const userId = user.id; // Menggunakan ID yang sudah dinormalisasi
    if (!userId) {
      console.error('User ID is missing for user:', user);
      return;
    }

    const response = await fetch(`/api/user/users/${userId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ role: newRole })
    });

    if (response.ok) {
      alert(`User role updated to ${newRole}`);
      user.role = newRole;
    } else {
      const err = await response.json();
      alert('Failed to update role: ' + (err.detail || 'Unknown error'));
    }
  } catch (error) {
    console.error('Error updating role:', error);
    alert('Error updating role');
  }
};

const fetchCases = async (page = 1) => {
  try {
    let url = `/api/case/cases?page=${page}&limit=${limit}`;
    if (filterCountry.value) url += `&country=${encodeURIComponent(filterCountry.value)}`;
    if (filterDriver.value) url += `&driver=${encodeURIComponent(filterDriver.value)}`;
    if (filterYear.value) url += `&year=${filterYear.value}`;
    
    console.log('Fetching URL:', url); // Debug log
    
    const response = await fetch(url);
    if (response.ok) {
      const result = await response.json();
      cases.value = result.data;
      totalItems.value = result.total;
      totalPages.value = Math.ceil(result.total / limit);
      currentPage.value = page;
    } else {
      alert('Failed to fetch data');
    }
  } catch (error) {
    console.error('Error fetching cases:', error);
    alert('Error fetching data');
  }
};

const clearFilters = async () => {
  filterCountry.value = '';
  filterDriver.value = '';
  filterYear.value = null;
  currentPage.value = 1;
  await fetchCases(1);
};

const createData = async () => {
  try {
    const payload = {
      country: createForm.country,
      driver: createForm.driver,
      losses: [{ year: createForm.year, tc_loss_ha: createForm.tc_loss_ha }],
      threshold: createForm.threshold
    };
    const response = await fetch('/api/case/cases', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (response.ok) {
      alert('Data added successfully');
      showCreateModal.value = false;
      fetchCases(currentPage.value);
    } else {
      const error = await response.json();
      alert('Failed to add data: ' + (error.detail || 'Unknown error'));
    }
  } catch (error) {
    console.error(error);
    alert('Error adding data');
  }
};

const editCase = (entry) => {
  editForm.id = entry.id;
  editForm.originalCountry = entry.country;
  editForm.originalDriver = entry.driver;
  editForm.originalYear = Number(entry.year);
  
  editForm.country = entry.country;
  editForm.driver = entry.driver;
  editForm.year = Number(entry.year);
  editForm.tc_loss_ha = entry.tc_loss_ha;
  editForm.threshold = entry.threshold;
  
  showEditModal.value = true;
};

const updateData = async () => {
  try {
    const payload = {
      id: editForm.id,
      country: editForm.originalCountry,
      driver: editForm.originalDriver,
      year: editForm.originalYear,
      new_data: { 
        country: editForm.country,
        driver: editForm.driver,
        year: editForm.year,
        tc_loss_ha: editForm.tc_loss_ha,
        threshold: editForm.threshold
      }
    };
    const response = await fetch('/api/case/cases', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (response.ok) {
      alert('Data updated successfully');
      showEditModal.value = false;
      fetchCases(currentPage.value);
    } else {
      const error = await response.json();
      alert('Failed to update data: ' + (error.detail || 'Unknown error'));
    }
  } catch (error) {
    console.error(error);
    alert('Error updating data');
  }
};

const deleteCase = async (entry) => {
  if (confirm(`Are you sure you want to delete data for ${entry.country} (${entry.year})?`)) {
    try {
      const params = new URLSearchParams({
        country: entry.country,
        driver: entry.driver,
        year: entry.year
      });
      const response = await fetch(`/api/case/cases?${params.toString()}`, {
        method: 'DELETE',
      });
      if (response.ok) {
        alert('Data deleted successfully');
        fetchCases(currentPage.value);
      } else {
        alert('Failed to delete data');
      }
    } catch (error) {
      console.error('Error deleting data:', error);
      alert('Error deleting data');
    }
  }
};

const goToPage = async (page) => {
  if (page >= 1 && page <= totalPages.value) {
    await fetchCases(page);
  }
};

const nextPage = async () => {
  if (currentPage.value < totalPages.value) {
    await fetchCases(currentPage.value + 1);
  }
};

const prevPage = async () => {
  if (currentPage.value > 1) {
    await fetchCases(currentPage.value - 1);
  }
};
</script>

<style scoped>
.modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1050;
}

.modal-content {
    background: white;
    border-radius: 0.5rem;
    max-width: 500px;
    width: 100%;
}
</style>