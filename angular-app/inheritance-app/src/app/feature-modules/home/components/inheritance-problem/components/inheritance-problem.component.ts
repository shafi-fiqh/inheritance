import {
  Component,
  ElementRef,
  EventEmitter,
  Input,
  OnChanges,
  OnInit,
  Output,
  SimpleChanges,
  ViewChild,
} from '@angular/core'
import { DROPDOWN_VALUES, GENDER } from '../constants/inheritor.constant'
import html2canvas from 'html2canvas'

@Component({
  selector: 'inheritance-problem-component',
  templateUrl: 'inheritance-problem.component.html',
  styleUrls: ['inheritance-problem.component.scss'],
})
export class InheritanceProblemComponent implements OnInit, OnChanges {
  @Input() problemSet: any
  @Input() wholeProblemList: any
  @Input() index: any
  @Input() loading: any
  @Input() error: any
  @Output() rightArrowClickEvent = new EventEmitter()
  @Output() leftArrowClickEvent = new EventEmitter()
  @ViewChild('table')
  table!: ElementRef
  @ViewChild('canvas') canvas!: ElementRef
  @ViewChild('downloadLink') downloadLink!: ElementRef
  isNestedSharesAccordionOpen = false
  isNestedProblemBase_1AccordionOpen = false
  isNestedProblemBase_2AccordionOpen = false
  isFinalSolutionAccordionOpen = false
  optionValues = DROPDOWN_VALUES
  keys: any
  GENDER = GENDER
  totalIntermediateShare: any
  grid = []

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['problemSet']) {
      this.grid = []
      this.keys = []
      this.onChanges()
    }
  }
  ngOnInit() {}
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
  getSharePoolTotal() {
    const totalPoolShare = this.problemSet?.intermediate_shares
      ?.inheritance_pool.total_shares
    let lastindex = this.problemSet?.intermediate_shares?.share_pool[
      totalPoolShare
    ]
    return lastindex
  }

  getFirstProblemSolution(values: any) {
    return this.problemSet?.intermediate_shares?.share_pool[values]
  }
  getGender(name: any) {
    // @ts-ignore
    return GENDER[name]
  }
  downloadTable() {
    const tableElement = this.table.nativeElement
    return new Promise<void>(async (resolve, reject) => {
      try {
        const canvas = await html2canvas(tableElement)
        this.canvas.nativeElement.src = canvas.toDataURL()
        this.downloadLink.nativeElement.href = canvas.toDataURL('image/png')
        this.downloadLink.nativeElement.download = `InheritanceProblem-${
          this.index === 0 ? '1' : this.index
        }.png`
        this.downloadLink.nativeElement.click()
        resolve()
      } catch (error) {
        reject(error)
      }
    })
  }
  onChanges() {
    this.keys = Object.keys(this.problemSet?.problem)
    this.totalIntermediateShare = this.getSharePoolTotal()
    if (
      this.getFirstProblemSolution(
        this.problemSet.intermediate_shares.inheritance_pool.remainder,
      ) !== 0 ||
      this.problemSet?.final_shares.remainder !== 0
    ) {
      // @ts-ignore
      this.grid.push(...this.keys, 'Remainder', 'Total')
    } else {
      // @ts-ignore
      this.grid.push(...this.keys, 'Total')
    }
    console.log(this.problemSet)
  }
}
