import { Routes } from '@angular/router';
import { AdminLoginComponent } from './admin/login/login.component';
import { HomeComponent } from './home/home.component';

export const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'admin/login', component: AdminLoginComponent },
  { path: 'admin/dashboard', loadComponent: () => import('./admin/dashboard/dashboard.component').then(m => m.AdminDashboardComponent) },
  { path: '**', redirectTo: '/home' }
];
