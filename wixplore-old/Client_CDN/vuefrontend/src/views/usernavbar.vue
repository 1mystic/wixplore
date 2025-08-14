<template>
  <div class="user-layout">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-top">
        <div class="logo-container">
          <img src="@/assets/sqlogo.svg" alt="logo" class="logo" />
        </div>
        <nav class="nav-links">
          <router-link to="/home" class="nav-link" active-class="active-link">
            <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
          </router-link>
          <router-link to="/cultural-map" class="nav-link" active-class="active-link" title="Cultural Map">
            <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/><circle cx="12" cy="9" r="2.5"/></svg>
          </router-link>
          <router-link to="/passport" class="nav-link" active-class="active-link" title="Global Passport">
            <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/><path d="M8 7h6"/><path d="M8 11h8"/><path d="M8 15h6"/></svg>
          </router-link>
          <router-link to="/summary" class="nav-link" active-class="active-link" title="Performance">
            <i class="bi bi-bar-chart-line" style="font-size: 1.55rem;"></i>             
          </router-link>
          <router-link to="/profile" class="nav-link" active-class="active-link" title="Profile">
            <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          </router-link>
          <router-link to="/report" class="nav-link" active-class="active-link" title="AI Report">
            <i class="bi bi-stars" style="font-size: 1.55rem;"></i>
          </router-link>
        </nav>
      </div>
      <div class="sidebar-bottom">
        <button class="nav-link" @click="goToBookmarks" title="Bookmarks">
          <svg xmlns="http://www.w3.org/2000/svg" width="23" height="23" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m19 21-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>
        </button>
        <button class="nav-link logout-btn" @click="handleLogout" title="Logout">
          <svg  width="25" height="25" viewBox="0 0 24 24" fill="none" stroke="rgb(148, 81, 98)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
      <div v-if="show_notification" class="notification-bar">
        <div class="notification">
          Nice work! You completed 2/5 quizzes this week
        </div>
      </div>
      <div class="user-content">
        <router-view></router-view>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'UserNavbar',
  data() {
    return {
      show_notification: false,
    }
  },
  methods: {
    goToBookmarks() {
      this.$router.push('/bookmarks')
    },
    async handleLogout() {
      try {
        await this.$store.dispatch('logoutUser')
        this.$router.push('/')
      } catch (error) {
        console.error('Logout failed:', error)
      }
    },
  },
}
</script>

<style scoped>
.user-layout {
  display: flex;
  min-height: 100vh;
  background: #f8f9fa;
}

.sidebar {
  position: fixed;
  width: 80px;
  height: 100vh;
  background: #f6ffe7;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  padding: 2rem 0 1.5rem 0;
  box-shadow: 2px 0 8px rgba(0,0,0,0.03);
  z-index: 10;
}
.logo-container {
  margin-bottom: 2rem;
  display: flex;
  justify-content: center;
}
.logo {
  width: 2.8vw;
  height: 2.8vw;
  border-radius: 5rem;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  padding: 0.4rem;
}
.nav-links {
  display: flex;
  flex-direction: column;
  gap: 2.2rem;
  align-items: center;
}
.nav-link {
  background: none;
  border: none;
  outline: none;
  color: #7a8a6e;
  font-size: 1.7rem;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: 10rem;
  margin-bottom: 0.2rem;
  transition: background 0.18s, color 0.18s;
  cursor: pointer;
}
.nav-link:hover, .nav-link.active-link, .router-link-exact-active {
  background: #e6f7c7;
  color: #3d4e2d;
}
.sidebar-bottom {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  align-items: center;
}
.logout-btn {
  color: #945162;
}
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: #f8f9fa;
  padding: 0 0 0 0;
  margin-left: 5rem;
}
.user-content {
  flex: 1;
  padding: 2.5rem 2.5rem 2.5rem 2.5rem;
  min-height: 0;
}
.notification-bar {
  width: 100%;
  background: #e6f7c7;
  color: #3d4e2d;
  padding: 0.7rem 2rem;
  border-radius: 0 0 12px 12px;
  margin-bottom: 1.5rem;
  font-weight: 500;
  box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}

@media (max-width: 900px) {
  .user-content {
    padding: 1rem;
  }
  .main-content {
    padding: 0;
  }
}
</style> 