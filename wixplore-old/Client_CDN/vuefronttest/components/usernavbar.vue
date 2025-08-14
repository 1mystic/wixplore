<template>
  <div class="user-nav">
    <nav class="navbar">
      <div class="nav-brand">
        <router-link to="/home">Quiz Master</router-link>
      </div>
      
      <div class="nav-links">
        <router-link to="/home" class="nav-link">
          <i class="fas fa-home"></i> Home
        </router-link>
        <router-link to="/bookmarks" class="nav-link">
          <i class="fas fa-bookmark"></i> Bookmarks
        </router-link>
        <router-link to="/cultural-map" class="nav-link">
          <i class="fas fa-globe-americas"></i> Cultural Map
        </router-link>
        <router-link to="/passport" class="nav-link">
          <i class="fas fa-passport"></i> Global Passport
        </router-link>
        <router-link to="/summary" class="nav-link">
          <i class="fas fa-chart-line"></i> Summary
        </router-link>
        <router-link to="/report" class="nav-link">
          <i class="fas fa-file-alt"></i> Reports
        </router-link>
        <router-link to="/profile" class="nav-link">
          <i class="fas fa-user"></i> Profile
        </router-link>
      </div>

      <div class="nav-actions">
        <button @click="logout" class="logout-btn">
          <i class="fas fa-sign-out-alt"></i> Logout
        </button>
      </div>
    </nav>

    <div class="content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserNavbar',
  methods: {
    async logout() {
      try {
        await fetch('/logout', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        localStorage.removeItem('token')
        this.$router.push('/login')
      } catch (error) {
        console.error('Error logging out:', error)
      }
    }
  }
}
</script>

<style scoped>
.user-nav {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  background: #fff;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-brand a {
  font-size: 1.5rem;
  font-weight: bold;
  color: #2c3e50;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
}

.nav-link {
  color: #666;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  transition: all 0.2s;
}

.nav-link:hover {
  background: #f8f9fa;
  color: #2c3e50;
}

.nav-link.router-link-active {
  background: #e3f2fd;
  color: #2196f3;
}

.nav-actions {
  display: flex;
  gap: 1rem;
}

.logout-btn {
  background: none;
  border: none;
  color: #666;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  transition: all 0.2s;
}

.logout-btn:hover {
  background: #ffebee;
  color: #f44336;
}

.content {
  flex: 1;
  padding: 2rem;
  background: #f8f9fa;
}
</style> 