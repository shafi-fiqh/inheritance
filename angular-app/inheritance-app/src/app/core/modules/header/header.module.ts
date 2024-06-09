import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { HeaderComponent } from './components/header.component';


@NgModule({
  declarations: [HeaderComponent],
  exports: [
    HeaderComponent
  ],
  imports: [
    CommonModule,
    RouterModule
  ]
})
export class HeaderModule { }
