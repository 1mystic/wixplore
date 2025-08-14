<template>
  <div class="cultural-context" v-if="context">
    <div class="context-header">
      <h3>Cultural Insight</h3>
      <div class="difficulty-badge" :class="difficultyClass">
        Level {{ context.difficulty_level }}
      </div>
    </div>
    <div class="context-content">
      <p>{{ context.cultural_context }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CulturalContext',
  props: {
    questionId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      context: null
    }
  },
  computed: {
    difficultyClass() {
      if (!this.context) return ''
      const level = this.context.difficulty_level
      return {
        'level-1': level === 1,
        'level-2': level === 2,
        'level-3': level === 3,
        'level-4': level === 4,
        'level-5': level === 5
      }
    }
  },
  async created() {
    await this.fetchContext()
  },
  methods: {
    async fetchContext() {
      try {
        const response = await fetch(`/api/questions/${this.questionId}/cultural-context`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        this.context = await response.json()
      } catch (error) {
        console.error('Error fetching cultural context:', error)
      }
    }
  }
}
</script>

<style scoped>
.cultural-context {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
  margin: 1rem 0;
  border-left: 4px solid #4CAF50;
}

.context-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.context-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.2rem;
}

.difficulty-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 600;
}

.level-1 {
  background: #E3F2FD;
  color: #1976D2;
}

.level-2 {
  background: #E8F5E9;
  color: #388E3C;
}

.level-3 {
  background: #FFF3E0;
  color: #F57C00;
}

.level-4 {
  background: #FCE4EC;
  color: #C2185B;
}

.level-5 {
  background: #F3E5F5;
  color: #7B1FA2;
}

.context-content {
  color: #546E7A;
  line-height: 1.6;
}

.context-content p {
  margin: 0;
}
</style> 