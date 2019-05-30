import { Component, OnInit } from '@angular/core';
import { addDays, format, startOfWeek } from 'date-fns';
import { Observable, of } from 'rxjs';
import { map } from 'rxjs/operators';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {
  public readonly appTitle = 'MensApp';
  public today = new Date();
  public startDate$: Observable<Date>;
  public endDate$: Observable<Date>;

  public days$: Observable<string[]>;
  public selectedDay = format(this.today, 'dddd');

  ngOnInit() {
    this.startDate$ = of(startOfWeek(this.today, { weekStartsOn: 1 }));
    this.endDate$ = this.startDate$.pipe(map(startDate => addDays(startDate, 4)));
    this.days$ = this.startDate$.pipe(
      map(startDate => {
        const days: string[] = [];
        for (let i = 0; i <= 5; i++) {
          days.push(format(addDays(startDate, i), 'dddd'));
        }

        return days;
      }),
    );
  }
}
