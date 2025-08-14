<template>
  <div class="region-view">
    <div class="region-header" v-if="region">
      <div class="region-title">
        <span class="region-flag">{{ region.flag_emoji }}</span>
        <h1>{{ region.name }}</h1>
      </div>
      <p class="region-description">{{ region.description }}</p>
    </div>

    <div class="region-content">
      <div class="subjects-section">
        <h2>Cultural Topics</h2>
        <div class="subjects-grid">
          <div v-for="subject in subjects" :key="subject.id" class="subject-card">
            <h3>{{ subject.name }}</h3>
            <p>{{ subject.description }}</p>
            <div class="cultural-context" v-if="subject.cultural_context">
              <p>{{ subject.cultural_context }}</p>
            </div>
            <div class="subject-actions">
              <button @click="viewChapters(subject.id)" class="btn-explore">
                Explore Topics
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="progress-section" v-if="userProgress">
        <h2>Your Progress in {{ region.name }}</h2>
        <div class="progress-stats">
          <div class="stat-card">
            <div class="stat-value">{{ userProgress.completedQuizzes }}</div>
            <div class="stat-label">Quizzes Completed</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{{ userProgress.averageScore }}%</div>
            <div class="stat-label">Average Score</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{{ userProgress.culturalPoints }}</div>
            <div class="stat-label">Cultural Points</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RegionView',
  data() {
    return {
      region: null,
      subjects: [],
      userProgress: null
    }
  },
  async created() {
    await this.fetchRegion()
    await this.fetchSubjects()
    await this.fetchUserProgress()
  },
  methods: {
    async fetchRegion() {
      try {
        const response = await fetch(`/api/regions/${this.$route.params.regionId}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        this.region = await response.json()
      } catch (error) {
        console.error('Error fetching region:', error)
      }
    },
    async fetchSubjects() {
      try {
        const response = await fetch(`/api/subjects/by-region/${this.$route.params.regionId}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        this.subjects = await response.json()
      } catch (error) {
        console.error('Error fetching subjects:', error)
      }
    },
    async fetchUserProgress() {
      // This would be implemented based on your backend API
      // For now, using mock data
      this.userProgress = {
        completedQuizzes: 5,
        averageScore: 85,
        culturalPoints: 250
      }
    },
    viewChapters(subjectId) {
      this.$router.push(`/chapters/${subjectId}`)
    }
  }
}
</script>

<style scoped>
.region-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.region-header {
  text-align: center;
  margin-bottom: 3rem;
}

.region-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.region-flag {
  font-size: 3rem;
}

.region-description {
  color: #666;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

.subjects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.subject-card {
  background: #fff;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.subject-card:hover {
  transform: translateY(-5px);
}

.subject-card h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.cultural-context {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  margin: 1rem 0;
  font-size: 0.9rem;
  color: #666;
}

.subject-actions {
  margin-top: 1.5rem;
}

.btn-explore {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-explore:hover {
  background: #388E3C;
}

.progress-section {
  margin-top: 4rem;
  padding-top: 2rem;
  border-top: 2px solid #eee;
}

.progress-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.stat-card {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 12px;
  text-align: center;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.stat-label {
  color: #666;
  font-size: 0.9rem;
}
</style> 