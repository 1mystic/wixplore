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
import { ref, computed, onMounted } from 'vue'

export default {
  name: 'CulturalContext',
  props: {
    questionId: {
      type: Number,
      required: true
    }
  },
  setup(props) {
    const context = ref(null)

    const difficultyClass = computed(() => {
      if (!context.value) return ''
      const level = context.value.difficulty_level
      return {
        'level-1': level === 1,
        'level-2': level === 2,
        'level-3': level === 3,
        'level-4': level === 4,
        'level-5': level === 5
      }
    })

    const fetchContext = async () => {
      try {
        const response = await fetch(`/api/questions/${props.questionId}/cultural-context`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        context.value = await response.json()
      } catch (error) {
        console.error('Error fetching cultural context:', error)
      }
    }

    onMounted(() => {
      fetchContext()
    })

    return {
      context,
      difficultyClass
    }
  }
}
</script>

<style scoped>
.cultural-context {
  background: #f8f9fa;
  border-radius: 0.8rem;
  padding: 1.5rem;
  margin: 1rem 0;
  border-left: 4px solid #4CAF50;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.cultural-context:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transform: translateX(4px);
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
  font-size: 1.3rem;
  font-weight: 600;
}

.difficulty-badge {
  padding: 0.4rem 1rem;
  border-radius: 1rem;
  font-size: 0.95rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.difficulty-badge:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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
  font-size: 1.05rem;
}

.context-content p {
  margin: 0;
}

@media (max-width: 768px) {
  .cultural-context {
    padding: 1.2rem;
  }

  .context-header h3 {
    font-size: 1.2rem;
  }

  .difficulty-badge {
    padding: 0.3rem 0.8rem;
    font-size: 0.9rem;
  }

  .context-content {
    font-size: 1rem;
  }
}
</style> 