import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {RoutingModule} from "@app/core/modules/routing/routing.module";
import {HeaderModule} from "@app/core/modules/header/header.module";
import { HttpClientModule } from "@angular/common/http";
import { BrowserAnimationsModule } from '@angular/platform-browser/animations'


@NgModule({
  declarations: [],
  imports: [
    CommonModule,
  ],
  exports: [
    RoutingModule,
    HeaderModule,
    HttpClientModule,
    BrowserAnimationsModule
  ]
})
export class CoreModule { }
