// store.js

const store = new Vuex.Store({
    state() {
        return {
            user: localStorage.getItem('user') || null,
            token: localStorage.getItem('token') || null,
            role: localStorage.getItem('role') || null,
            count: 0,
            bookmarkedQuizzes: JSON.parse(localStorage.getItem('bookmarkedQuizzes')) || []           

        };
    
    },
    mutations: {
        toggle_bookmarkm(state, quizId) {
            const index = state.bookmarkedQuizzes.indexOf(quizId);
            if (index === -1) {
                state.bookmarkedQuizzes.push(quizId);
            } else {
                state.bookmarkedQuizzes.splice(index, 1);
            }
            localStorage.setItem('bookmarkedQuizzes', JSON.stringify(state.bookmarkedQuizzes));
        },

        setUser(state, user) {
            state.user = user;
            if (user) {
                localStorage.setItem('user', user);
            } else {
                localStorage.removeItem('user');
            }

        },
        setToken(state, token) {
            state.token = token;
            if (token) {
                localStorage.setItem('token', token);
            } else {
                localStorage.removeItem('token');
            }
        },
        setRole(state, role) {
            state.role = role;
            if (role) {
                localStorage.setItem('role', role);
            } else {
                localStorage.removeItem('role');
            }
        },
        clearAuth(state) {
            state.user = null;
            state.token = null;
            state.role = null;
            localStorage.removeItem('token');
            localStorage.removeItem('role');
            localStorage.removeItem('user');
        },
        increment(state) {
            state.count++;
        } 
       
    },
    actions: {
        
        toggleQuizBookmark({ commit }, quizId) {
            commit('toggle_bookmarkm', quizId);
        },

        notify_user({ commit }) {
            commit('set_notify');
        },
        seen_notify({ commit }) {
            commit('clear_notify');
        },

        async loginUser({ commit }, credentials) {
            try {
                const response = await fetch('http://127.0.0.1:5000/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(credentials)
                });

                const data = await response.json();

                if (response.ok) {
                   
                    commit('setToken', data.access_token);
                    commit('setRole', data.role);
                    commit('setUser', data.username);
                    return { success: true, role: data.role };
                } else {
                    throw new Error(data.message);
                }
            } catch (error) {
                throw error;
            }
        },
        async logoutUser({ commit, state }) {
            try {
                await fetch('http://127.0.0.1:5000/logout', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${state.token}`
                    }
                });
                commit('clearAuth');
                

                return true;
            } catch (error) {
                console.error('Logout error:', error);
                throw error;
            }
        },
        checkAuth({ state, commit }) {
            const token = state.token;
            const role = state.role;
            
            if (!token || !role) {
                commit('clearAuth');
                return false;
            }
            return { token, role };
        },
        incrementAsync({ commit }) {
            setTimeout(() => {
                commit('increment');
            }, 1000);
        }
    },
    getters: {
        isAuthenticated: state => !!state.token,
        userRole: state => state.role,
        getToken: state => state.token,
        getUser: state => state.user,
        doubleCount: (state) => state.count * 2,
        getBookmarkedQuizIds: state => state.bookmarkedQuizzes,
        isQuizBookmarked: state => quizId => state.bookmarkedQuizzes.includes(quizId)


    }
});