import { Component, OnInit } from '@angular/core';
import {Item} from '../../models/Item';
import {ActivatedRoute} from '@angular/router';
import {ItemsService} from '../../services/items.service';

@Component({
  selector: 'app-search-results',
  templateUrl: './search-results.component.html',
  styleUrls: ['./search-results.component.css']
})
export class SearchResultsComponent implements OnInit {

  query: string;
  results: Item[] = [];

  constructor(private route: ActivatedRoute, private itemService: ItemsService) { }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.query = params.q;
      this.itemService.getSearchResults(this.query).subscribe(response => {
        this.results = response;
        console.log(this.results);
      });
    });
  }

  isNew(item: Item): boolean {
    const dateThreshold = new Date(new Date().getTime() - (7 * 24 * 60 * 60 * 1000));
    return new Date(item.insertDate) > dateThreshold;
  }

}
