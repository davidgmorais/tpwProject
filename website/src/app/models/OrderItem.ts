import { Cart } from './Cart';
import { Item } from './Item';

export class OrderItem {
  id: number;
  item: Item | number;
  cart: number;
  qty: number;
}
