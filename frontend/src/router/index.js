import Vue from 'vue'
import Router from 'vue-router'
import store from '../store'
import ClassroomTable from '@/components/pages/ClassroomTable'
import SignIn from '@/components/pages/SignIn'
import Register from '@/components/pages/Register'
import Profile from '@/components/pages/Profile'
import Classroom from '@/components/pages/Classroom'
import Invitation from '@/components/pages/CreateAccountInvitation'
import ResetPassword from '@/components/pages/ResetPassword'

Vue.use(Router)

const router = new Router({
    routes: [
        {
            path: '/signin',
            name: 'SignIn',
            component: SignIn,
            meta: {
                public: true
            }
        },
        {
            path: '/login',
            redirect: '/signin',
            meta: {
                public: true
            }
        },
        {
            path: '/register',
            name: 'Register',
            component: Register,
            meta: {
                public: true
            }
        },
        {
            path: '/profile',
            name: 'Profile',
            component: Profile
        },
        {
            path: '/',
            name: 'ClassroomTable',
            component: ClassroomTable
        },
        {
            path: '/classroom',
            name: 'Classroom',
            component: Classroom
        },
        {
            path: '/shell',
            redirect: '/'
        },
        {
            path: '/home',
            redirect: '/'
        },
        {
            path: '/invitation',
            name: 'Invitation',
            component: Invitation
        },
        {
            path: '/reset-password/:uidb64/:token/',
            name: 'reset',
            component: ResetPassword,
            meta: {
                public: true
            }
        }
    ]
})

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.public)) {
        next()
    } else {
        if (store.state.auth.status.loggedIn) {
            next()
            return
        }
        next('/signin')
    }
})

export default router
