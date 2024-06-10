import { Component, OnInit } from '@angular/core'
import { Problem_Set } from '@app/stubData/inheritance-generator'
import { InheritanceStore } from './store/inheritance-generator.store'

@Component({
  selector: 'home-component',
  template: `
  <div class="flex justify-center">
    <inheritance-problem-component
      [problemSet]="problemSet[index]"
      [index]= "index"
      (rightArrowClickEvent)="nextProblem()"
      (leftArrowClickEvent)="previousProblem()"
    ></inheritance-problem-component>
    </div>
  `,
    providers: [InheritanceStore]
})
export class HomeComponent implements OnInit{
  constructor(private inheritanceStore : InheritanceStore){}
  problems$ = this.inheritanceStore.problems$;
  loading$ = this.inheritanceStore.loading$;
  error$ = this.inheritanceStore.error$;
  problemSet = Problem_Set
  index = 0
  ngOnInit() {
   // this.inheritanceStore.fetchProblems();
  }

  nextProblem() {
    this.index < this.problemSet.length ? this.index++ : this.index
  }
  previousProblem() {
    this.index > 0 ? this.index-- : this.index
  }
}
