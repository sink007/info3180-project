import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import RegisterView from '../views/RegisterView.vue';
import LoginView from '../views/LoginView.vue';
import AboutView from '../views/AboutView.vue';
import ReportView from '../views/ReportView.vue';
import ProfilesView from '../views/ProfilesView.vue';
import ProfileDetailView from '../views/ProfileDetailView.vue';
import FavouritesView from '../views/FavouritesView.vue';
import MyProfileView from '../views/MyProfileView.vue';
import CreateProfileView from '../views/CreateProfileView.vue';
import MatchesView from '../views/MatchesView.vue';

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/about', name: 'about', component: AboutView },
  { path: '/register', name: 'register', component: RegisterView },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/report', name: 'report', component: ReportView },
  { path: '/profiles', name: 'profiles', component: ProfilesView },
  { path: '/profiles/:id', name: 'profile-detail', component: ProfileDetailView },
  { path: '/favourites', name: 'favourites', component: FavouritesView },
  { path: '/profiles/matches/:id', name: 'matches', component: MatchesView },
  { path: '/my-profile', name: 'my-profile', component: MyProfileView },
  { path: '/profiles/new', name: 'new-profile', component: CreateProfileView }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;