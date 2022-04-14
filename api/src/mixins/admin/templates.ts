import {ReccApiBase} from '../../reccApiBase';
import type {TemplateA} from '../../packet/template';

export class ReccApiAdminTemplates extends ReccApiBase {
  getAdminTemplates() {
    return this.get<Array<TemplateA>>('/admin/templates');
  }
}
