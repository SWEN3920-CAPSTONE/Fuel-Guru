import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import LoginView from '../views/LoginView.vue'
import SignupView from '../views/SignupView.vue'
import MapView from '../views/MapView.vue'
import FuelPricesView from '../views/FuelPricesView.vue'
import GasStationView from '../views/GasStationView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomeView
    },
    {
      path: '/about-us',
      name: 'About',
      component: AboutView
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginView
    },    
    {
      path: '/signup',
      name: 'Signup',
      component: SignupView
    },    
    {
      path: '/map',
      name: 'Map',
      component: MapView
    },    
    {
      path: '/fuelPrices',
      name: 'FuelPrices',
      component: FuelPricesView
    },
    {
      path: '/gasstations',
      name: 'GasStation',
      component: GasStationView
    },
  ]
})

export default router
