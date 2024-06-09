// src/app/inheritance/inheritance.store.ts
import { Injectable } from '@angular/core'
import { ComponentStore } from '@ngrx/component-store'
import { Observable } from 'rxjs'
import { switchMap, tap } from 'rxjs/operators'
import { DataFetcher } from '@app/shared/service/dataFetcher.service'
import { inheritanceGeneratorAPI } from '@app/shared/service/constants/api.constants'

interface InheritanceState {
  problems: any[]
  loading: boolean
  error: string | null
}

@Injectable()
export class InheritanceStore extends ComponentStore<InheritanceState> {
  constructor(private dataFetcher: DataFetcher) {
    super({ problems: [], loading: false, error: null })
  }

  readonly problems$ = this.select((state) => state.problems)
  readonly loading$ = this.select((state) => state.loading)
  readonly error$ = this.select((state) => state.error)

  // Updaters
  readonly setLoading = this.updater((state, loading: boolean) => ({
    ...state,
    loading,
  }))

  readonly setError = this.updater((state, error: string | null) => ({
    ...state,
    error,
  }))

  readonly setProblems = this.updater((state, problems: any[]) => ({
    ...state,
    problems,
  }))

  // Effects
  readonly fetchProblems = this.effect((trigger$: Observable<void>) =>
    trigger$.pipe(
      tap(() => {
        this.setLoading(true)
        this.setError(null)
      }),
      switchMap(() =>
        this.dataFetcher
          .fetch(inheritanceGeneratorAPI, 'post', {
            must_haves: ['father', 'mother', 'daughter', 'son'],
            not_haves: ['father_of_father'],
            n_types: 5,
            grandfather_and_siblings: 'false',
          })
          .pipe(
            tap({
              next: (problems) => {
                this.setProblems(problems)
                this.setLoading(false)
              },
              error: (error) => {
                this.setError(error.message)
                this.setLoading(false)
              },
            }),
          ),
      ),
    ),
  )
}
