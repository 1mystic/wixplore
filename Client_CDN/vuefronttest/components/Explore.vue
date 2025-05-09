<template>
  <div class="explore">
    <div class="hero-section">
      <h1>Explore Global Knowledge</h1>
      <p>Discover cultures, earn points, and expand your horizons</p>
    </div>

    <div class="features-grid">
      <div class="feature-card" @click="$router.push('/cultural-map')">
        <div class="feature-icon">🌍</div>
        <h3>Cultural Map</h3>
        <p>Explore your journey through different regions and cultures</p>
      </div>

      <div class="feature-card" @click="$router.push('/passport')">
        <div class="feature-icon">📚</div>
        <h3>Global Passport</h3>
        <p>Track your cultural exploration progress and earned badges</p>
      </div>

      <div class="feature-card" @click="$router.push('/summary')">
        <div class="feature-icon">📊</div>
        <h3>Knowledge Summary</h3>
        <p>View your learning progress and achievements</p>
      </div>
    </div>

    <div class="regions-section">
      <h2>Explore Regions</h2>
      <div class="regions-grid">
        <div v-for="region in regions" 
             :key="region.id" 
             class="region-card"
             @click="$router.push(`/regions/${region.id}`)">
          <div class="region-flag">{{ region.flag_emoji }}</div>
          <h3>{{ region.name }}</h3>
          <p>{{ region.description }}</p>
        </div>
      </div>
    </div>

    <div class="recent-activity">
      <h2>Recent Activity</h2>
      <div class="activity-list">
        <div v-for="activity in recentActivity" 
             :key="activity.id" 
             class="activity-card">
          <div class="activity-icon">{{ activity.icon }}</div>
          <div class="activity-content">
            <h4>{{ activity.title }}</h4>
            <p>{{ activity.description }}</p>
            <span class="activity-time">{{ activity.time }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Explore',
  data() {
    return {
      regions: [],
      recentActivity: [
        {
          id: 1,
          icon: '🏆',
          title: 'Earned Cultural Master Badge',
          description: 'Completed Asian History quiz with 95% score',
          time: '2 hours ago'
        },
        {
          id: 2,
          icon: '🌍',
          title: 'Explored European Region',
          description: 'Completed 5 quizzes in European History',
          time: '1 day ago'
        },
        {
          id: 3,
          icon: '⭐',
          title: 'Earned 150 Cultural Points',
          description: 'Mastered African Geography topics',
          time: '2 days ago'
        }
      ]
    }
  },
  async created() {
    await this.fetchRegions()
  },
  methods: {
    async fetchRegions() {
      try {
        const response = await fetch('/api/regions', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        this.regions = await response.json()
      } catch (error) {
        console.error('Error fetching regions:', error)
      }
    }
  }
}
</script>

<style scoped>
.explore {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.hero-section {
  text-align: center;
  margin-bottom: 3rem;
}

.hero-section h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.hero-section p {
  color: #666;
  font-size: 1.2rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 4rem;
}

.feature-card {
  background: #fff;
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.feature-card p {
  color: #666;
}

.regions-section {
  margin-bottom: 4rem;
}

.regions-section h2 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 2rem;
}

.regions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.region-card {
  background: #fff;
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s;
}

.region-card:hover {
  transform: translateY(-5px);
}

.region-flag {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.region-card h3 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.region-card p {
  color: #666;
  font-size: 0.9rem;
}

.recent-activity {
  margin-top: 4rem;
}

.recent-activity h2 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 2rem;
}

.activity-list {
  display: grid;
  gap: 1.5rem;
}

.activity-card {
  background: #fff;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.activity-icon {
  font-size: 2rem;
}

.activity-content {
  flex: 1;
}

.activity-content h4 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.activity-content p {
  color: #666;
  margin-bottom: 0.5rem;
}

.activity-time {
  color: #999;
  font-size: 0.9rem;
}
</style> 