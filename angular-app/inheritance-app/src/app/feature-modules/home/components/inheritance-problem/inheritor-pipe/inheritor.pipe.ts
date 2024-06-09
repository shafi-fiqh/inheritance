import { Pipe, PipeTransform } from "@angular/core";
import { INHERITOR_CONST } from "../constants/inheritor.constant";

@Pipe({ name: 'inheritorPipe' })
export class InheritorPipe implements PipeTransform {
    transform(inheritor: any) {
      return (INHERITOR_CONST[inheritor] ?? 'A Family Member');
    }
  }