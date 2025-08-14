<template>
        <div class="component-wrapper">

<!-- Unified Search -->
<div class="panel_enc">
    <div class="search_enc">
        <div class="search_enc">
            <input 
                type="text" 
                v-model="searchQuery"
                placeholder="Search Chapters..."
                class="search_input"
            >
            
        </div>
    </div>
     <select v-model="selectedSubject" 

        class="unified_search__select"

        @change="filterBySubject">



        <option value="">All Subjects</option>

        <option v-for="subject in subjects" 

            :key="subject.id" 

            :value="subject.id">

        {{ subject.name }}

        </option>

    </select>
    <button class="add_button" @click="openModal">
        <i class="fas fa-plus"></i>
        <span>Add Chapter</span>
    </button>
</div>          


   
  
<!-- Chapters Table -->
<div class="admin_table_enc">
    <table class="admin_table">
        <thead>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Subject</th>
                <th>Description</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="chapter in filteredChapters" :key="chapter.id">
                <td>{{ chapter.id }}</td>
                <td>{{ chapter.name }}</td>
                <td>{{ getSubjectName(chapter.subject_id) }}</td>
                <td>{{ chapter.description }}</td>
                <td>
                    <button @click="editChapter(chapter)">
                        <i class="fas fa-edit"></i> Edit
                    </button>
                    <button @click="deleteChapter(chapter.id)">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                    <button @click="addquiz(chapter)">
                        <i class="fas fa-plus"></i> Quiz
                    </button>
                </td>
            </tr>
        </tbody>
    </table>
</div>

<!-- Modal -->
<div class="modal fade" id="chapterModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">{{ isEditing ? 'Edit Chapter' : 'Add Chapter' }}</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <form @submit.prevent="isEditing ? updateChapter() : saveChapter()">
                    <div class="mb-3">
                        <label class="form-label">Chapter Name</label>
                        <input type="text" class="form-control" v-model="currentChapter.name" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Subject</label>
                        <select class="form-control" v-model="currentChapter.subject_id" required>
                            <option v-for="subject in subjects" 
                                    :key="subject.id" 
                                    :value="subject.id">
                                {{ subject.name }}
                            </option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Description</label>
                        <textarea class="form-control" v-model="currentChapter.description" rows="3"></textarea>
                    </div>
                    <button type="submit" class="modal_submit">Save Changes</button>
                </form>
            </div>
        </div>
    </div>
</div>

<!-- Quiz Modal -->
<div class="modal fade" id="quizModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Add Quiz</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <form @submit.prevent="addQuiz()">
                    <div class="mb-3">
                        <label class="form-label">Quiz Title</label>                                  

                        <input type="text" class="form-control" v-model="newQuiz.title" required>
                    </div>     
                    
                    <div class="mb-3">
                        <label class="form-label">Chapter</label>
                        <input type="text" class="form-control" v-model="newQuiz.chapter_name" required disabled>
                        <input type="hidden" v-model="newQuiz.chapter_id" required disabled>
                    </div>
                   
                    <div class="mb-3">
                        <label class="form-label">Duration (minutes)</label>
                        <input type="number" class="form-control" v-model="newQuiz.duration_minutes" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Deadline</label>
                        <input type="datetime-local" class="form-control" v-model="newQuiz.date_of_quiz" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Release At</label>
                        <input type="datetime-local" class="form-control" v-model="newQuiz.release_at" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Remarks</label>
                        <textarea class="form-control" v-model="newQuiz.remarks" rows="3"></textarea>
                    </div>
                    <button type="submit" class="modal_submit">Add Quiz</button>
                </form>
            </div>
        </div>
    </div>
</div>

</div>
    `,
</template>

<script>
export default {
  name: 'Chapters',
  data() {
        return {
            chapters: [],
            subjects: [],
            currentChapter: {
                id: null,
                name: '',
                subject_id: '',
                description: ''
            },
            newQuiz: {
                title: '',
                chapter_id: '',
                chapter_name: '',
                duration_minutes: '',
                date_of_quiz: '',
                remarks: '',
                release_at: ''
            },
            selected_chapter : '',
            selectedSubject: '',
            isEditing: false,
            searchQuery: '',
            loading: false,
            error: null,
            modalInstance: null
        }
    },
    computed: {
        filteredChapters() {
            let filtered = this.chapters;
            
            if (this.selectedSubject) {
                filtered = filtered.filter(chapter => 
                    chapter.subject_id === this.selectedSubject
                );
            }
            
            if (this.searchQuery) {
                const query = this.searchQuery.toLowerCase().trim();
                filtered = filtered.filter(chapter => 
                    chapter.name.toLowerCase().includes(query) ||
                    chapter.description?.toLowerCase().includes(query) ||
                    this.getSubjectName(chapter.subject_id).toLowerCase().includes(query)
                );
            }
            
            return filtered;
        }
    },
    methods: {
        
        getSubjectName(subjectId) {
            const subject = this.subjects.find(s => s.id === subjectId);
            return subject ? subject.name : 'Unknown Subject';
        },
        filterBySubject() {
            // This method can be used to add additional filtering logic if needed
        },
        openModal() {
            this.isEditing = false;
            this.currentChapter = { id: null, name: '', subject_id: '', description: ''};
            new bootstrap.Modal(document.getElementById('chapterModal')).show();
        },
        addquiz(chapter) {
            this.newQuiz.chapter_id = chapter.id;
            this.newQuiz.chapter_name = chapter.name;
            this.selected_chapter = chapter.id;
            new bootstrap.Modal(document.getElementById('quizModal')).show();
        },

        editChapter(chapter) {
            this.isEditing = true;
            this.currentChapter = { ...chapter };
            new bootstrap.Modal(document.getElementById('chapterModal')).show();            
        },
        // CRUD operations
        async fetchSubjects() {
            try {
                const response = await fetch('http://127.0.0.1:5000/api/subjects', {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });
                if (!response.ok) {
                    throw new Error('Failed to fetch subjects');
                }
                this.subjects = await response.json();
            } catch (error) {
                this.showNotification('error', error.message);
            }
        },
        async fetchChapters() {
            this.loading = true;
            try {
                const response = await fetch('http://127.0.0.1:5000/api/chapters', {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });
                if (!response.ok) {
                    throw new Error('Failed to fetch chapters');
                }
                this.chapters = await response.json();
                if (!Array.isArray(this.chapters)) {
                    throw new Error('Invalid response from server');
                }
            } catch (error) {
                this.error = error.message;
            } finally {
                this.loading = false;
            }
        },
        async saveChapter() {
            if (!this.currentChapter.name || !this.currentChapter.subject_id) {
                return this.showNotification('error', 'Chapter name and subject are required');
            }
            try {
                const response = await fetch('http://127.0.0.1:5000/api/chapters', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    },
                    body: JSON.stringify({                        
                        name: this.currentChapter.name,
                        subject_id: this.currentChapter.subject_id,
                        description: this.currentChapter.description
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.message || 'Failed to add chapter');
                }

                this.showNotification('success', 'Chapter added successfully');
                await this.fetchChapters();
                this.closeModal();
            } catch (error) {
                this.showNotification('error', error.message);
            }
        },
        async updateChapter() {
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/chapters/${this.currentChapter.id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    },
                    body: JSON.stringify({
                        name: this.currentChapter.name,
                        subject_id: this.currentChapter.subject_id,
                        description: this.currentChapter.description
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.message || 'Failed to update chapter');
                }

                this.showNotification('success', 'Chapter updated successfully');
                await this.fetchChapters();
                this.closeModal();
            } catch (error) {
                this.showNotification('error', error.message);
            }
        },
        async deleteChapter(id) {
            if (!confirm('Are you sure you want to delete this chapter?')) return;

            try {
                const response = await fetch(`http://127.0.0.1:5000/api/chapters/${id}`, {    
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`,
                        'Content-Type': 'application/json'
                    }
                });

                if (!response.ok) {
                    if (response.status === 404) {
                        throw new Error('Chapter not found');
                    }
                    throw new Error('Failed to delete chapter');
                }

                this.showNotification('success', 'Chapter deleted successfully');
                await this.fetchChapters();
            } catch (error) {
                this.showNotification('error', error.message);
                console.error('Delete error:', error);
            }
        },
        async addQuiz() {
            try {
                
                const response = await fetch('http://127.0.0.1:5000/api/quizzes', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    },
                    body: JSON.stringify(this.newQuiz)
                });

                if (!response.ok) throw new Error('Failed to create quiz');

                this.showNotification('success', 'Quiz created successfully');
                
                this.closeModal();
            } catch (error) {
                this.showNotification('error', error.message);
            }
        },

        closeModal() {
            this.modalInstance?.hide();
            this.resetForm();
        },
        resetForm() {
            this.currentChapter = { id: null, name: '', subject_id: '', description: '' };
            this.isEditing = false;
            this.error = null;
        },
        showNotification(type, message) {
            const notification = document.createElement('div');
            notification.className = `notification ${type}`;
            notification.innerText = message;

            Object.assign(notification.style, {
                position: 'fixed',
                bottom: '20px',
                left: '20px',
                padding: '10px 20px',
                backgroundColor: type === 'success' ? 'green' : 'red',
                color: 'white',
                borderRadius: '5px',
                zIndex: 1000,
                opacity: 0,
                transition: 'opacity 0.5s'
            });

            document.body.appendChild(notification);

            requestAnimationFrame(() => {
                notification.style.opacity = 1;
            });

            setTimeout(() => {
                notification.style.opacity = 0;
                notification.addEventListener('transitionend', () => {
                    notification.remove();
                });
            }, 3000);
        }
    },
    mounted() {
        this.fetchSubjects();
        this.fetchChapters();
    }
}
</script>

<style scoped>

.modal_submit {
    padding: 0.5rem 1rem;
    background-color:rgba(228, 72, 72, 0.84);
    color: white;
    border: none;
    border-radius: 3rem;
    cursor: pointer;
    transition: all 0.3s ease;
    width: 100%;
    font-weight: 600;
}
    .modal_submit:hover {
        background-color:rgba(192, 35, 100, 0.8);
    }


    .subj_btn {
        padding: 5px 10px;
        font-size: 0.9rem;
        max-width: 6rem;
        max-height: 3rem;
        background-color:rgb(231, 250, 209);
        color: #000;
        border-radius: 8px;
        border: none;
    }

    .panel_enc {
    display: flex;
    justify-content: left;
    align-items: center;
    padding: 1.5rem;
    margin: 1rem 0;    
    border-radius: 12px;    
    gap: 1rem;
    }

    .search_enc {
        flex: 1;
        max-width: 500px;
    }

    .search_sec {
        position: relative;
        width: 100%;
    }

    .search_input {
        width: 100%;
        padding: 0.8rem 1rem 0.8rem 2.5rem;
        border: 4px solid rgba(199, 195, 195, 0.77);
        border-radius: 7rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }

    .search_input:focus {
        border-color:rgba(226, 74, 119, 0.89);        
        outline: none;
    }

    .search_icon {
        position: absolute;
        right : 0.8rem;
        top: 50%;
        transform: translateY(-50%);
        color: #666;
        font-size: 1rem;
    }
        
    .add_button {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border: 5px solid rgb(73, 72, 71);
        background-color: rgb(189, 243, 178);
        border-radius: 7rem;
        color: black;
        font-size: 1rem;
        font-weight: 500;
        cursor: pointer;
        max-width: 12rem;
        transition: all 0.3s ease;
    }

    .add_button:hover {        
       
        background-color: rgb(202, 230, 137);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    .add_button i {
        font-size: 0.9rem;
    }

.admin_table {
width: 100%;
border-collapse: collapse;
margin-top: 1rem;

}
.admin_table thead {
    background-color:rgba(226, 174, 158, 0.92);
    color: white;
}

.admin_table thead th:first-child {
    border-top-left-radius: 0.5rem;
}

.admin_table thead th:last-child {
    border-top-right-radius: 0.5rem;
}

.admin_table tbody tr:nth-child(even) {
    background-color: rgb(247, 252, 234);
}

.admin_table th,
.admin_table td {
    padding: 1rem;
    text-align: left;
    color : #3d3d3d;
    font-size: 1rem;
    font-family: 'Lexend Deca', sans-serif;
}

.admin_table button {

display: inline-block;
text-align: center;
padding: 0.4rem 1rem;
font-size: 0.8rem;
background-color:  rgba(143, 83, 79, 0.27);
border-radius: 5rem;
border: 1px solid transparent ;
margin: 0.4rem;
color: rgb(63, 55, 55);
cursor: pointer;
transition: all 0.3s ease;
}

.admin_table button:hover {
background-color: rgba(255, 105, 105, 0.82);
}




    /* Responsive Design */
    @media (max-width: 768px) {
        .control-panel {
            flex-direction: column;
            padding: 1rem;
        }

        .search_sec {
            width: 100%;
            max-width: 100%;
            margin-bottom: 1rem;
        }

        .add_button {
            width: 100%;
            justify-content: center;
        }
    }
       



unified_search__select{    
    padding: 0.6rem 0.8rem;
    border: 5px solid rgba(238, 223, 223, 0.59);
    background-color: rgb(233, 243, 178);
    border-radius: 7rem;        
    }

    .btn-clear {
    padding: 0.5rem 1rem;
    font-size: 1rem;
    font-weight: 600;
    max-width: 6rem;
    max-height: 4rem;
    background-color: rgb(243, 255, 235);
    border : 4px solid rgba(236, 216, 216, 0.84);
    border-radius: 7rem;
}
    .btn-clear:hover {
    background-color: rgb(216, 212, 212);
    color: #000;

    /* question buttons in add quiz modal
    */

  
}


.unified_search__select{    
    padding: 0.6rem 0.8rem;
    border: 5px solid rgba(238, 223, 223, 0.59);
    background-color: rgb(233, 243, 178);
    border-radius: 7rem;        
    }

    .btn-clear {
    padding: 0.5rem 1rem;
    font-size: 1rem;
    font-weight: 600;
    max-width: 6rem;
    max-height: 4rem;
    background-color: rgb(243, 255, 235);
    border : 4px solid rgba(236, 216, 216, 0.84);
    border-radius: 7rem;
}
    .btn-clear:hover {
    background-color: rgb(216, 212, 212);
    color: #000;

    /* question buttons in add quiz modal
    */

  
}

</style>
