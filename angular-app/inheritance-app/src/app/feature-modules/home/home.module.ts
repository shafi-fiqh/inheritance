import { NgModule } from "@angular/core";
import { Routes, RouterModule } from "@angular/router";
import { HomeComponent } from "./components/home-page/home.component";
import { InheritanceProblemComponent } from "./components/inheritance-problem/components/inheritance-problem.component";
import { CommonModule } from "@angular/common";
import { FormsModule } from "@angular/forms";
import { InheritorPipe } from "./components/inheritance-problem/inheritor-pipe/inheritor.pipe";
import { DataFetcher } from "@app/shared/service/dataFetcher.service";

const routes: Routes = [
  {
    path: '',
    component: HomeComponent
  },
];

@NgModule({
  declarations: [
    HomeComponent, 
    InheritanceProblemComponent,
    InheritorPipe
  ],
  imports: [
CommonModule,
FormsModule,
    RouterModule.forChild(routes),
  ],
  providers : [InheritorPipe, DataFetcher]
})
export class HomeModule { }
