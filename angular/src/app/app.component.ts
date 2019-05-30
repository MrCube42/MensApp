import { Component, OnInit } from '@angular/core';
import { addDays, startOfWeek } from 'date-fns';
import { Observable, of } from 'rxjs';
import { map } from 'rxjs/operators';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {
  public readonly appTitle = 'MensApp';
  public startDate$: Observable<Date>;
  public endDate$: Observable<Date>;

  ngOnInit() {
    const now = new Date();
    this.startDate$ = of(startOfWeek(now, { weekStartsOn: 1 }));
    this.endDate$ = this.startDate$.pipe(map(startDate => addDays(startDate, 4)));
  }
}
