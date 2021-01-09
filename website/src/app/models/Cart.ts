import {Item} from './Item';

export class Cart {
  items: Item[];
  user: string;

  total(): number {
    let total = 0;
    for (const item of this.items) {
      total += item.finalPrice();
    }
    return total;
  }
}
