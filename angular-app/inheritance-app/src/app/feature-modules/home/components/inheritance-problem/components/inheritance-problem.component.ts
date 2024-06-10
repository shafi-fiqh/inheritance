import {
  Component,
  EventEmitter,
  Input,
  OnInit,
  Output,
} from '@angular/core'
import { DROPDOWN_VALUES, GENDER } from '../constants/inheritor.constant'
import { animate, state, style, transition, trigger } from '@angular/animations'


@Component({
  selector: 'inheritance-problem-component',
  templateUrl: 'inheritance-problem.component.html',
  styleUrls: ['inheritance-problem.component.scss'],
})
export class InheritanceProblemComponent implements OnInit {
  @Input() problemSet: any
  @Input() index = 0
  @Output() rightArrowClickEvent = new EventEmitter()
  @Output() leftArrowClickEvent = new EventEmitter()
  isNestedSharesAccordionOpen = false
  isNestedProblemBase_1AccordionOpen = false
  isNestedProblemBase_2AccordionOpen = false
  isFinalSolutionAccordionOpen = false
  optionValues = DROPDOWN_VALUES
  keys : any
  GENDER= GENDER
  totalIntermediateShare : any
  ngOnInit() {
    this.totalIntermediateShare = this.getSharePoolTotal()
}
  rightArrowClicked() {
    this.isNestedSharesAccordionOpen = false
    this.isNestedProblemBase_1AccordionOpen = false
    this.isNestedProblemBase_2AccordionOpen = false
    this.isFinalSolutionAccordionOpen = false
    this.rightArrowClickEvent.emit()
  }

  leftArrowClicked() {
    this.isNestedSharesAccordionOpen = false
    this.isNestedProblemBase_1AccordionOpen = false
    this.isNestedProblemBase_2AccordionOpen = false
    this.isFinalSolutionAccordionOpen = false
    this.leftArrowClickEvent.emit()
  }
  getSharePoolTotal(){
    const newArray = Object.keys(this.problemSet?.intermediate_shares?.share_pool)
    let lastindex = newArray.pop()
return lastindex
  }
}