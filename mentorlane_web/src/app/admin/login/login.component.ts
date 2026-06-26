import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-admin-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class AdminLoginComponent {
  username: string = '';
  password: string = '';
  rememberMe: boolean = false;
  isLoading: boolean = false;
  errorMessage: string = '';

  constructor(private router: Router) {}

  onLogin(): void {
    // Reset error message
    this.errorMessage = '';
    
    // Basic validation
    if (!this.username || !this.password) {
      this.errorMessage = 'Please enter both username and password';
      return;
    }

    // Set loading state
    this.isLoading = true;

    // Simulate API call (replace with actual authentication logic)
    setTimeout(() => {
      // Demo authentication - replace with real authentication
      if (this.username === 'admin' && this.password === 'admin123') {
        // Store authentication token (in a real app, use proper auth service)
        if (this.rememberMe) {
          localStorage.setItem('adminToken', 'demo-token');
        } else {
          sessionStorage.setItem('adminToken', 'demo-token');
        }
        
        // Navigate to admin dashboard
        this.router.navigate(['/admin/dashboard']);
      } else {
        this.errorMessage = 'Invalid username or password';
        this.isLoading = false;
      }
    }, 1000);
  }
}