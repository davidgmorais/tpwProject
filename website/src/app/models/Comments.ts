import {Item} from './Item';
import {Profile} from './Profile';

export class Comments {
  id: number;
  item: Item;
  user: Profile;
  text: string;
  stars: number;

}
