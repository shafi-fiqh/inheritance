import { Component, ElementRef, EventEmitter, Input, OnInit, Output, ViewChild } from "@angular/core";
import { DROPDOWN_VALUES } from "../constants/inheritor.constant";

@Component({
    selector: 'inheritance-problem-component',
    templateUrl: 'inheritance-problem.component.html',
    styleUrls: ['inheritance-problem.component.scss'],
})
export class InheritanceProblemComponent implements OnInit {
    @Input() problemSet: any
    @Output() rightArrowClickEvent = new EventEmitter()
    @Output() leftArrowClickEvent = new EventEmitter()
    isNestedAccordionOpen = false 
    optionValues = DROPDOWN_VALUES
    ngOnInit() {
    }
rightArrowClicked(){
    this.rightArrowClickEvent.emit()
}

leftArrowClicked(){
    this.leftArrowClickEvent.emit()
}
  
}
