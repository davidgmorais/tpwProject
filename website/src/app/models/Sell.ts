import {Item} from './Item';
import {Profile} from './Profile';

export class Sell {
  id: number;
  item: Item;
  moneyReceived: number;
  pendingSell: boolean;
  accepted: boolean;
  user: Profile;
}
