import { Component, OnDestroy, OnInit } from '@angular/core'
import { Problem_Set } from '@app/stubData/inheritance-generator'
import { InheritanceStore } from './store/inheritance-generator.store'
import { Subscription } from 'rxjs';

@Component({
  selector: 'home-component',
  template: `
  <div class="flex justify-center">
    <inheritance-problem-component
      [problemSet]="problemSet[index]"
      [loading]="loading$ | async"
      [error] ="error$ | async"
      [wholeProblemList]="problemSet"
      [index]= "index"
      (rightArrowClickEvent)="nextProblem()"
      (leftArrowClickEvent)="previousProblem()"
    ></inheritance-problem-component>
    </div>
  `,
    providers: [InheritanceStore]
})
export class HomeComponent implements OnInit, OnDestroy{
  constructor(private inheritanceStore : InheritanceStore){}
  problems$ = this.inheritanceStore.problems$;
  loading$ = this.inheritanceStore.loading$;
  error$ = this.inheritanceStore.error$;
  problemSet = Problem_Set
  index = 0
  subscriptions = new Subscription()
  ngOnInit() {
    this.inheritanceStore.fetchProblems();
    this.subscriptions.add(this.problems$.subscribe(problem =>{
      console.log(problem)
     }))
  }

  nextProblem() {
    this.index < this.problemSet.length-1 ? this.index++ : this.index
  }
  previousProblem() {
    this.index > 0 ? this.index-- : this.index
  }

  ngOnDestroy() {
    this.subscriptions.unsubscribe()
  }
}
