import {Item} from './Item';
import {Profile} from './Profile';

export class Purchase {
  id: number;
  item: Item;
  price: number;
  user: Profile;
  discountedP: boolean;
}
