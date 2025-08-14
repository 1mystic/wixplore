<template>  <!-- Search button -->
  <!-- Search and Filters -->
      <div class="filter_bar">
          <div class="search_bar">
              <i class="fas fa-search"></i>
              <input 
                  type="text" 
                  v-model="searchQuery" 
                  placeholder="Search quizzes..."
                  class="form-control"
              >
          </div>
     
      
          <div class="filter_opt">                      
              <div class="form-check form-switch" 
                  style="margin-top: 0.8rem;">
              <input class="form-check-input" type="checkbox" id="flexSwitchCheckDefault"
                  v-model="hideExpired" @change="filterQuizzes">
              <label class="form-check-label" 
              style="font-size: 1.2rem;
                      margin-top: 0.2rem;"
              for="flexSwitchCheckDefault">Exclude Expired</label>
              </div>
          </div>
      </div>
  
   <!-- Bookmarked Quizzes -->
    <h2 class="section-title">Bookmarked Quizzes</h2>
    <div
      class="slider-container"
      id="quizSlider"               
      ref="sliderContainer"
    >
      <div class="slider-navigation">
        <button class="slider-nav slider-prev" id="sliderPrev">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-arrow-left"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
        </button>
        <button class="slider-nav slider-next" id="sliderNext">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-arrow-right"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
        </button>
      </div>
      <div class="slider-track" ref="sliderTrack">
        <div v-for="quiz in displayedQuizzes" :key="quiz.id" class="quiz-card-wrapper">
          <div class="quiz-card" :class="{ 'selected': selectedSubject === quiz.subject_id }">
            <div class="quiz-card-image">
              <div class="bookmark-icon" :class="{ 'bookmarked': isBookmarked(quiz.id) }" @click="toggleBookmark(quiz.id)">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" :fill="isBookmarked(quiz.id) ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m19 21-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>
              </div>
              <div class="quiz-card-img-title" :title="quiz.title">
                <span class="clamp-2">{{ quiz.title }}</span>
              </div>
            </div>
            <div class="quiz-meta-info">
              <div class="quiz-meta-title">
                <span class="quiz-meta-subject" :title="getSubjectName(getChapter(quiz.chapter_id)?.subject_id)">
                  <i class="bi bi-journal-minus"></i> <span class="clamp-1">{{ getSubjectName(getChapter(quiz.chapter_id)?.subject_id) }}</span>
                </span>
                <span class="quiz-meta-chapter" :title="getChapterName(quiz.chapter_id)">
                  <i class="bi bi-book-half"></i> <span class="clamp-1">{{ getChapterName(quiz.chapter_id) }}</span>
                </span>
              </div>
            </div>
            <div class="quiz-meta-row">
              <i class="bi bi-clock"></i>
              <span class="quiz-subtitle">{{ formatDuration(quiz.time_duration) }}</span>
              <span class="quiz-subtitle">{{ quiz.question_count }} Questions</span>
            </div>
            <div class="quiz-info">
              <button @click="startQuiz(quiz.id)" class="quiz-action" :disabled="isPastQuiz(quiz.date_of_quiz)">
                {{ isPastQuiz(quiz.date_of_quiz) ? 'Expired' : 'Attempt Quiz' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>




       

  
  <!-- Quiz Categories -->
  <h2 class="section-title"></h2> <!-- Quiz Categories -->
  <div class="categories-grid">
      <div 
        v-for="subject in subjects" 
        :key="subject.id" 
        class="category-card subject-card"
        @click="selectSubject(subject)"
        :class="{ 'selected': selectedSubject === subject.id }"
      >
       
            <div class="category-icon">
            <i class="bi bi-journal-minus"  style="font-size:1.5rem; font-weight:700;"></i>
            </div>
            <span>{{subject.name}}</span>
      </div>
      <div 
        v-for="chapter in chapters" 
        :key="chapter.id" 
        class="category-card chapter-card"
        @click="selectChapter(chapter)"
        :class="{ 'selected': selectedChapter === chapter.id }"
      >
       
            <div class="category-icon">
            <i class="bi bi-book-half" style="font-size:1.2rem;"></i>
            </div>
            <span>{{chapter.name}}</span>
      </div>
      
  </div>

</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

export default {
  name: 'Bookmarks',
  data() {
    return {
      
       
      // API Data
    
      subjects: [],
      chapters: [],
      selectedSubject: '',
      selectedChapter: '',
      searchQuery: '',
      hideExpired: false,
      loading: false,
      userName: 'Student',
      userEmail: '',         
      availableQuizzes: [],
     
     


    };
  },
  computed: {
    filteredChapters() {
        if (!this.selectedSubject) return this.chapters;
        return this.chapters.filter(chapter => 
            chapter.subject_id === this.selectedSubject
        );
    },
    displayedQuizzes() {
        const bookmarkedIds = this.$store.getters.getBookmarkedQuizIds;
        let filtered = this.availableQuizzes.filter(quiz => bookmarkedIds.includes(quiz.id));
        
        
        // subj filter
        if (this.selectedSubject) {
            filtered = filtered.filter(quiz => {
                const chapter = this.getChapter(quiz.chapter_id);
                return chapter && chapter.subject_id === this.selectedSubject;
            });
        }
        
        // ch fitler
        if (this.selectedChapter) {
            filtered = filtered.filter(quiz => 
                quiz.chapter_id === this.selectedChapter
            );
        }
        
        // search query filter
        if (this.searchQuery.trim()) {
            const query = this.searchQuery.toLowerCase();
            filtered = filtered.filter(quiz => 
                quiz.title.toLowerCase().includes(query) ||
                this.getChapterName(quiz.chapter_id).toLowerCase().includes(query) ||
                this.getSubjectName(this.getChapter(quiz.chapter_id)?.subject_id).toLowerCase().includes(query)
            );
        }

        // expired filter
        if (this.hideExpired) {
            filtered = filtered.filter(quiz => !this.isPastQuiz(quiz.date_of_quiz));
        }
        
        return filtered;
    }
},
async created() {
 
  await Promise.all([
      this.fetchSubjects(),
      this.fetchChapters(),
      this.fetchQuizzes()
  ]);
},

  methods: {

    toggleBookmark(quizId) {
      this.$store.dispatch('toggleQuizBookmark', quizId);
    },
    isBookmarked(quizId) {
      return this.$store.getters.isQuizBookmarked(quizId);
    },


   

    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('en-US', {
          day: 'numeric',
          month: 'short',
          year: 'numeric'
      });
  },

  formatDuration(duration) {
      const minutes = duration.split(':')[1];
      return `${minutes} mins`;
  },

    getSubjectName(subjectId) {
      return this.subjects.find(subject => subject.id === subjectId)?.name || '';
      },
      getChapterName(chapterId) {
          return this.chapters.find(chapter => chapter.id === chapterId)?.name || '';
      },
     
      async fetchSubjects() {
          try {
              const response = await fetch('http://127.0.0.1:5000/api/subjects', {
                  headers: {
                      'Authorization': `Bearer ${this.$store.state.token}`
                  }
              });
              if (response.ok) {
                  this.subjects = await response.json();
              }
          } catch (error) {
              console.error('Error fetching subjects:', error);
          }
      },
      async fetchChapters() {
          try {
              const response = await fetch('http://127.0.0.1:5000/api/chapters', {
                  headers: {
                      'Authorization': `Bearer ${this.$store.state.token}`
                  }
              });
              if (response.ok) {
                  this.chapters = await response.json();
              }
          } catch (error) {
              console.error('Error fetching chapters:', error);
          }
      },
      async fetchQuizzes() {
          try {
              const response = await fetch('http://127.0.0.1:5000/api/quizzes', {
                  headers: {
                      'Authorization': `Bearer ${this.$store.state.token}`
                  }
              });
              if (response.ok) {
                  const quizzes = await response.json();
                  this.availableQuizzes = quizzes.filter(quiz => {
                      // Parse the release_at string into a Date object
                      const releaseDate = new Date(quiz.release_at);

                      // Compare release_date with the current date/time
                      return releaseDate <= new Date(); // new Date() returns the current date/time
                  });

                  console.log(this.availableQuizzes); // Quizzes that have been released
                  console.log(new Date()); // Current date/time
              }
          } catch (error) {
              console.error('Error fetching quizzes:', error);
          }
      },
      formatDuration(duration) {
          const minutes = duration.split(':')[1];
          return `${minutes} mins`;
      },
      isPastQuiz(quizDate) {
          return new Date(quizDate) < new Date();
      },
      getChapter(chapterId) {
          return this.chapters.find(chapter => chapter.id === chapterId);
      },
      startQuiz(quizId) {
       const old_quiz = this.userScores.find(quiz => quiz.quiz_id === quizId);
       if (old_quiz) {
           alert("You have already attempted this quiz.");
           return;
       }        
      window.open(this.$router.resolve({ path: `/quiz/${quizId}` }).href, '_blank');
  },
      filterQuizzes() {
          this.fetchQuizzes();
      },
    
    selectSubject(subject) {
      this.selectedSubject = this.selectedSubject === subject.id ? null : subject.id;
      this.selectedChapter = null; // Deselect chapter when subject changes
    },
    selectChapter(chapter) {
      this.selectedChapter = this.selectedChapter === chapter.id ? null : chapter.id;
      this.selectedSubject = null; // Deselect subject when chapter changes
    },

  },

  mounted() {
    this.fetchUserScores();
    this.fetchSubjects();
    this.fetchChapters();
    this.fetchQuizzes();
   
    
  },

  // Use beforeUnmount (Vue 3) or beforeDestroy (Vue 2)
  beforeUnmount() {
    this.cleanup();
  },

};
</script>

<style scoped>


/* --- Filter Bar Container --- */
.filter_bar {
    display: flex;
    flex-wrap: wrap; /* Allows items to wrap on smaller screens */
    align-items: center;
    gap: 1.5rem; /* Space between search bar and filter option */
    padding: 1.5rem 2rem; /* Adjust padding as needed */
    margin-bottom: 0.5rem; /* Space below the filter bar */
}

/* --- Search Bar Styling --- */
.search_bar {
    display: flex;
    align-items: center;
    background-color: #ffffff;              /* theme-input-bg */
    border: 1px solidrgb(250, 193, 193);          /* theme-input-border */
    border-radius: 0.8rem;          /* theme-border-radius */
    padding: 0.75rem 1rem; /* Inner padding */
    flex-grow: 1; /* Allows search bar to take available space */
    min-width: 280px; /* Minimum width before wrapping */
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
    height: 3.5rem; /* Height of the search bar */
}

.search_bar:focus-within {
    border-color: #a5d6a7;  /* theme-primary-green-darker */
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.07), 0 0 0 0.2rem rgba(165, 214, 167, 0.35); /* theme-box-shadow, theme-primary-green-rgb for focus ring */
}

.search_bar i.fas.fa-search {
    color: #795548;            /* theme-icon-color */
    font-size: 1rem; /* Adjust icon size */
    margin-right: 0.8rem; /* Space between icon and input text */
}

.search_bar input.form-control { /* Overriding Bootstrap .form-control */
    flex-grow: 1;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
    background-color: transparent !important;
    padding: 0 !important; /* Padding is handled by .search_bar */
    margin: 0 !important;
    font-size: 0.95rem;
    color: #5d4037;            /* theme-text-color */
    height: auto !important; /* Reset Bootstrap height constraints */
    line-height: 1.5; /* Ensure text is vertically centered */
}

.search_bar input.form-control::placeholder {
    color: #a0a0a0;     /* theme-placeholder-color */
    opacity: 1; /* Ensure placeholder is visible */
}

/* --- Filter Option (Exclude Expired Toggle) --- */
.filter_opt {
    display: flex;
    align-items: center;
}

.filter_opt .form-check.form-switch {
    display: flex;
    align-items: center;
    gap: 0.7rem; /* Space between Bootstrap switch and its label */
    padding-left: 0; /* Override Bootstrap's default padding */
}

.filter_opt .form-check-input { /* Styling Bootstrap's switch */
    width: 3.2em;  /* Custom width for the switch */
    height: 1.6em; /* Custom height */
    margin-left: 0; /* Override Bootstrap margin */
    background-color: #d8dde2;          /* toggle-inactive-bg */
    border: 1px solid #ced4da;           /* toggle-inactive-border */
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='-4 -4 8 8'%3e%3ccircle r='3' fill='white'/%3e%3c/svg%3e"); /* White thumb */
    background-position: 0.25em center; /* Initial position of the thumb */
    background-repeat: no-repeat;
    border-radius: 1.6em; /* Fully rounded track */
    box-shadow: inset 0 1px 2px rgba(0,0,0,0.1);
    transition: background-color 0.2s ease-in-out, background-position 0.2s ease-in-out, border-color 0.2s ease-in-out;
    cursor: pointer;
}

.filter_opt .form-check-input:checked {
    background-color: #a5d6a7;  /* toggle-active-bg (theme-primary-green-darker) */
    border-color: #a5d6a7;     /* toggle-active-bg (theme-primary-green-darker) */
    background-position: calc(100% - 0.25em) center; /* Thumb to the right */
}

.filter_opt .form-check-input:focus {
    border-color: #a5d6a7;  /* theme-primary-green-darker */
    box-shadow: inset 0 1px 2px rgba(0,0,0,0.1), 0 0 0 0.2rem rgba(165, 214, 167, 0.35); /* theme-primary-green-rgb for focus ring */
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='-4 -4 8 8'%3e%3ccircle r='3' fill='white'/%3e%3c/svg%3e"); /* Ensure thumb is visible on focus */
}

.filter_opt .form-check-label {
    font-size: 0.95rem;
    color: #5d4037;            /* theme-text-color */
    cursor: pointer;
    user-select: none; /* Prevent text selection on click */
    padding-top: 0.1em; /* Slight adjustment for better vertical alignment with the switch */
}

/* --- Responsive Adjustments --- */
@media (max-width: 768px) {
    .filter_bar {
        flex-direction: column; /* Stack items vertically */
        align-items: stretch;   /* Make items take full available width */
        padding: 1rem 1.5rem;
    }

    .search_bar {
        min-width: 0; /* Allow it to shrink */
        width: 100%;  /* Take full width when stacked */
    }

    .filter_opt {
        justify-content: flex-start; /* Align toggle to the left */
        width: 100%;
        margin-top: 1rem; /* Add space if search bar is above */
    }
}

@media (max-width: 480px) {
    .filter_bar {
        padding: 1rem;
        gap: 1rem;
    }

    .search_bar {
        padding: 0.6rem 0.8rem;
    }

    .search_bar input.form-control,
    .filter_opt .form-check-label {
        font-size: 0.9rem;
    }

    .filter_opt .form-check-input {
        width: 3em;
        height: 1.5em;
        border-radius: 1.5em;
    }
}

.section-title {
  font-size: 2.95rem;
  font-weight: 600;
  margin-bottom: 2rem;
  margin-top: 4rem;
  margin-left: 2rem;
  color: rgba(110, 79, 50, 0.73);
}

/* Slider styles */
.slider-container {
  position: relative;
  width: 100%;
  overflow: hidden;
  padding-bottom: 1rem;
}

.slider-track {
  display: flex;
  gap: 1.2rem;
  transition: transform 0.5s cubic-bezier(.77,0,.18,1);
  scroll-snap-type: x mandatory;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

/* Navigation buttons */
.slider-navigation {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  pointer-events: none;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 10;
}

.slider-nav {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.28);
  border: 1px solid rgba(255, 255, 255, 0.5);
  color: rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  pointer-events: auto;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;

}

.slider-nav:hover {
  background-color: #f5f5f5;
  transform: scale(1.05);
  color: rgba(0, 0, 0, 0.8);
}

.slider-prev {
  margin-left: 2rem;
}

.slider-next {
  margin-right: 2rem;
}

.quiz-card-wrapper {
  flex: 0 0 300px;
  max-width: 300px;
  min-width: 260px;
  display: flex;
  align-items: stretch;
}

.quiz-card {
  display: flex;
  flex-direction: column;
  height: 340px;
  justify-content: space-between;
  position: relative;
  background: #f8f9fa;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.06);
  border: 2px solid transparent;
  padding: 1.2rem 1rem 1rem 1rem;
  transition: transform 0.18s, box-shadow 0.18s, background 0.18s;
  cursor: pointer;
  scroll-snap-align: start;
}

.quiz-card:hover {
  background: #e6f7c7;
  transform: translateY(-4px) scale(1.04);
  box-shadow: 0 4px 12px rgba(76,175,80,0.10);
  border-color: #b2e59e;
}

.quiz-card-image {
  width: 100%;
  height: 80px;
  background-color: rgb(255, 162, 146);
  border-radius: 6px;
  margin-bottom: 0.7rem;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.quiz-card-img-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: rgba(0, 0, 0, 0.7);
  font-family: var(--font-content);
  width: 100%;
  text-align: center;
  margin: 0 auto;
  padding: 0.2rem 0.3rem;
  line-height: 1.2;
  white-space: normal;
  overflow: hidden;
}

.clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  max-height: 2.7em;
}

.clamp-1 {
  display: block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

.quiz-meta-info {
  margin-bottom: 0.3rem;
}

.quiz-meta-title {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
  align-items: flex-start;
}

.quiz-meta-subject, .quiz-meta-chapter {
  font-size: 0.98rem;
  color: #4e5d6c;
  font-family: var(--font-content);
  font-weight: 500;
  margin-bottom: 0.1rem;
  width: 100%;
}

.quiz-meta-subject i, .quiz-meta-chapter i {
  margin-right: 0.3rem;
  color: #b2e59e;
}

.quiz-meta-row {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  font-size: 0.98rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.bookmark-icon {
  position: absolute;
  top: 8px;
  right: 8px;
  background-color: #fff;
  border-radius: 50%;
  padding: 6px;
  cursor: pointer;
  z-index: 2;
  box-shadow: 0 2px 6px rgba(0,0,0,0.07);
  transition: background 0.18s, box-shadow 0.18s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bookmark-icon:hover {
  background-color: #e6f7c7;
  box-shadow: 0 4px 12px rgba(76,175,80,0.10);
}

.bookmark-icon.bookmarked svg {
  color: #4CAF50;
}

@media (max-width: 900px) {
  .section-title { font-size: 2rem; margin-left: 1rem; }
  .quiz-card-wrapper { flex: 0 0 70vw; max-width: 90vw; min-width: 60vw; }
  .quiz-card { height: 300px; padding: 1rem 0.5rem 0.8rem 0.5rem; }
  .quiz-card-img-title { font-size: 1rem; }
  .slider-nav { width: 32px; height: 32px; }
}
@media (max-width: 600px) {
  .section-title { font-size: 1.3rem; margin-left: 0.5rem; }
  .quiz-card-wrapper { flex: 0 0 90vw; max-width: 98vw; min-width: 80vw; }
  .quiz-card { height: 240px; padding: 0.5rem 0.2rem 0.5rem 0.2rem; }
  .quiz-card-img-title { font-size: 0.9rem; }
  .slider-track { gap: 0.5rem; }
  .slider-nav { width: 28px; height: 28px; }
  .filter_bar { flex-direction: column; gap: 0.7rem; padding: 0.7rem 0.5rem; }
  .search_bar { min-width: 0; width: 100%; padding: 0.5rem 0.3rem; }
  .filter_opt { width: 100%; margin-top: 0.5rem; }
  .categories-grid { grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 0.5rem; }
}

/* Category cards */
.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.category-card {
  border: 3px solid rgba(139, 229, 252, 0.14);
  border-radius: 8px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
  .subject-card {
  background-color: rgba(255, 235, 168, 0.26);
}



.chapter-card {
  background-color: rgba(114, 226, 226, 0.22);
}

.selected {
  background-color: rgba(132, 240, 155, 0.82); /*rgba(191, 255, 132, 0.62);*/
  border: 2px solid #333;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transform: scale(1.05);
}




.category-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.08);
}

.category-icon {
  width: 40px;
  height: 40px;
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.score_card_id {
  font-size: 3.5rem;
  font-weight: 700;
  color : rgba(0, 0, 0, 0.182);
  
}
/* Journey cards */
.journey-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.journey-card {
  border: 5px solid #e5e5e5;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  background-color: rgba(255, 255, 255, 0.8);
}
.journey-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transform: translateY(-4px);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
  background-color: rgba(255, 177, 163, 0.35);
  border: 5px solid rgba(73, 70, 69, 0.35);
}

.journey-image {
  width: 120px;
  min-width: 120px;
  background-color:rgb(220, 255, 181);
  display: flex;
  align-items: center;
  justify-content: center;
 
}

.journey-content {
  padding: 1rem;
  flex: 1;
}

.journey-title {
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.journey-subtitle {
  color: #666;
  font-size: 1.875rem;
  margin-bottom: 1rem;
}

.exp_progress-bar {
  width: 100%;
  height: 4px;
  background-color: #f0f0f0;
  border-radius: 2px;
  margin-bottom: 0.5rem;
}

.exp_progress-value {
  height: 100%;
  background-color: #333;
  border-radius: 2px;
}

.exp_progress-label {
  font-size: 0.75rem;
  color: #666;
}

/* Search button */
.search-button {
  display: flex;
  align-items: center;
  justify-content: felx-start;
  padding: 0.75rem 1.5rem;
 
  border-radius: 4px;
  margin: 2rem 1rem;
  max-width: 300px;
  cursor: pointer;
}

.search-icon {
  margin-right: 0.5rem;
}

.search-button:hover {
  background-color: #e0e0e0;
}

.mr-2 {
  margin-right: 0.5rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .sidebar {
    width: 60px;
  }
  
  .main-content {
    margin-left: 60px;
    width: calc(100% - 60px);
    padding: 1.5rem;
  }
  
  .categories-grid {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  }
  
  .journey-container {
    grid-template-columns: 1fr;
  }

  .slider-nav {
    width: 36px;
    height: 36px;
  }
  
  .slider-prev {
    margin-left: -10px;
  }
  
  .slider-next {
    margin-right: -10px;
  }
}

@media (max-width: 480px) {
  .sidebar {
    width: 50px;
  }
  
  .main-content {
    margin-left: 50px;
    width: calc(100% - 50px);
    padding: 1rem;
  }
  
  .quiz-card {
    min-width: 240px;
  }
  
  .journey-image {
    width: 80px;
    min-width: 80px;
  }

  .slider-nav {
    width: 32px;
    height: 32px;
  }
}

</style>
