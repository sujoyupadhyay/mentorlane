import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class AdminDashboardComponent {
  constructor(private router: Router) {}

  onLogout(): void {
    // Clear authentication tokens
    localStorage.removeItem('adminToken');
    sessionStorage.removeItem('adminToken');
    
    // Navigate to login page
    this.router.navigate(['/admin/login']);
  }
}