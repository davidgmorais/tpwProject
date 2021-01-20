import {Item} from './Item';
import {User} from './User';

export class Purchase {
  id: number;
  item: Item;
  price: number;
  user: User;
  discountedP: boolean;
}
