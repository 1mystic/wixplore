import { createRouter, createWebHashHistory } from 'vue-router'
import store from '../store'

// Lazy load components
const Land = () => import('../views/Land.vue')
const Admin = () => import('../views/admin.vue')
const AdminDash = () => import('../views/admin/Adash.vue')
const Subjects = () => import('../views/admin/Subjects.vue')
const Quizes = () => import('../views/admin/Quizes.vue')
const Chapters = () => import('../views/admin/Chapters.vue')
const Questions = () => import('../views/admin/Questions.vue')
const TrackUsers = () => import('../views/admin/TrackUsers.vue')
const QuizView = () => import('../views/QuizView.vue')
const Scores = () => import('../views/user_score.vue')
const UserNavbar = () => import('../views/usernavbar.vue')
const Explore = () => import('../views/user/Explore.vue')
const Bookmarks = () => import('../views/user/Bookmarks.vue')
const UserSummary = () => import('../views/user/UserSummary.vue')
const Profile = () => import('../views/user/Profile.vue')
const Report = () => import('../views/user/Report.vue')
const GlobalPassport = () => import('../views/user/GlobalPassport.vue')
const RegionView = () => import('../views/user/RegionView.vue')
const CulturalMap = () => import('../views/user/CulturalMap.vue')
const Login = () => import('../views/Login.vue')
const Signup = () => import('../views/Signup.vue')
const NotFound = () => import('../views/HandleNo.vue')

const router = createRouter({
  history: createWebHashHistory(),
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { top: 0 }
  },
  routes: [
    {
      path: '/',
      component: Land,
      beforeEnter: async (to, from, next) => {
        const auth = await store.dispatch('checkAuth')
        if (auth && auth.token) {
          next(auth.role === 'admin' ? '/admin/dash' : '/home')
        } else {
          next()
        }
      }
    },
    {
      path: '/admin',
      component: Admin,
      name: 'admin',
      meta: { requiresAuth: true, role: 'admin' },
      children: [
        {
          path: 'dash',
          component: AdminDash,
          name: 'adash'
        },
        {
          path: 'subjects',
          component: Subjects,
          name: 'subjects'
        },
        {
          path: 'quizes',
          component: Quizes,
          name: 'quizes'
        },
        {
          path: 'chapters',
          component: Chapters,
          name: 'chapters'
        },
        {
          path: 'questions',
          component: Questions,
          name: 'questions'
        },
        {
          path: 'tusers',
          component: TrackUsers,
          name: 'track-users'
        }
      ]
    },
    {
      path: '/quiz/:quizid(\\d+)',
      component: QuizView,
      name: 'quiz',
      meta: { requiresAuth: true, role: 'user' }
    },
    {
      path: '/scores/:Id(\\d+)',
      component: Scores,
      name: 'user_score',
      meta: { requiresAuth: true, role: 'user' }
    },
    {
      path: '/users',
      component: UserNavbar,
      name: 'usernavbar',
      meta: { requiresAuth: true, role: 'user' },
      children: [
        {
          path: '/home',
          component: Explore,
          name: 'explore',
          meta: { requiresAuth: true, role: 'user' }
        },
        {
          path: '/bookmarks',
          component: Bookmarks,
          name: 'bookmarks',
          meta: { requiresAuth: true, role: 'user' }
        },
        {
          path: '/summary',
          component: UserSummary,
          name: 'summary',
          meta: { requiresAuth: true, role: 'user' }
        },
        {
          path: '/profile',
          component: Profile,
          name: 'profile',
          meta: { requiresAuth: true, role: 'user' }
        },
        {
          path: '/report',
          component: Report,
          name: 'report',
          meta: { requiresAuth: true, role: 'user' }
        },
        {
          path: '/passport',
          component: GlobalPassport,
          name: 'passport',
          meta: { requiresAuth: true, role: 'user' }
        },
        {
          path: '/regions/:regionId',
          component: RegionView,
          name: 'region',
          meta: { requiresAuth: true, role: 'user' }
        },
        {
          path: '/cultural-map',
          component: CulturalMap,
          name: 'cultural-map',
          meta: { requiresAuth: true, role: 'user' }
        }
      ]
    },
    {
      path: '/login',
      component: Login,
      name: 'login',
      beforeEnter: async (to, from, next) => {
        const auth = await store.dispatch('checkAuth')
        if (auth && auth.token) {
          next(auth.role === 'admin' ? '/admin/dash' : '/home')
        } else {
          next()
        }
      }
    },
    {
      path: '/signup',
      component: Signup,
      name: 'signup'
    },
    {
      path: '/:catchAll(.*)',
      component: NotFound,
      name: 'notfound'
    }
  ]
})

// Navigation guards
router.beforeEach(async (to, from, next) => {
  console.log(`Navigating from ${from.path} to ${to.path}`)

  if (to.matched.some(record => record.meta.requiresAuth)) {
    const auth = await store.dispatch('checkAuth')
    
    if (!auth || !auth.token) {
      next({ path: '/login', query: { redirect: to.fullPath } })
    } else {
      if (to.matched.some(record => record.meta.role === auth.role)) {
        next()
      } else {
        next(auth.role === 'admin' ? '/admin/dash' : '/home')
      }
    }
  } else {
    next()
  }
})

router.afterEach((to, from) => {
  console.log(`Navigation completed to ${to.path}`)
})

export default router 