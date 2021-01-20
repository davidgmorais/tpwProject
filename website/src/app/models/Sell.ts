import {Item} from './Item';
import {User} from './User';

export class Sell {
  id: number;
  item: Item;
  moneyReceived: number;
  pendingSell: boolean;
  accepted: boolean;
  user: User;
}
