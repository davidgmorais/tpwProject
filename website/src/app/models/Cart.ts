import {Item} from './Item';
import {Profile} from './Profile';

export class Cart {
  id: number;
  user: Profile;

  /*total(): number {
    let total = 0;
    for (const item of this.items) {
      total += item.finalPrice();
    }
    return total;
  }*/
}
