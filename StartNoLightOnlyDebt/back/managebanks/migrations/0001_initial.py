# Generated by Django 4.2.16 on 2024-11-19 05:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FinancialCompany',
            fields=[
                ('company_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('company_name', models.CharField(max_length=255, null=True)),
                ('homp_url', models.URLField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FinancialProduct',
            fields=[
                ('product_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=255, null=True)),
                ('join_way', models.CharField(max_length=255, null=True)),
                ('loan_inci_expn', models.TextField(null=True)),
                ('erly_rpay_fee', models.TextField(null=True)),
                ('dly_rate', models.TextField(null=True)),
                ('loan_lmt', models.CharField(max_length=255, null=True)),
                ('dcls_month', models.CharField(max_length=6, null=True)),
                ('dcls_strt_day', models.DateField(null=True)),
                ('dcls_end_day', models.DateField(null=True)),
                ('fin_co_subm_day', models.DateTimeField(null=True)),
                ('prdt_div', models.CharField(max_length=1, null=True)),
                ('fin_co_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='managebanks.financialcompany')),
            ],
        ),
        migrations.CreateModel(
            name='MortgageOption',
            fields=[
                ('option_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('dcls_month', models.CharField(max_length=6, null=True)),
                ('mrtg_type', models.CharField(max_length=1, null=True)),
                ('mrtg_type_nm', models.CharField(max_length=255, null=True)),
                ('rpay_type', models.CharField(max_length=1, null=True)),
                ('rpay_type_nm', models.CharField(max_length=255, null=True)),
                ('lend_rate_type', models.CharField(max_length=1, null=True)),
                ('lend_rate_type_nm', models.CharField(max_length=255, null=True)),
                ('lend_rate_min', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('lend_rate_max', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('lend_rate_avg', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('fin_prdt_cd', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='managebanks.financialproduct')),
            ],
        ),
        migrations.CreateModel(
            name='JeonseOption',
            fields=[
                ('option_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('dcls_month', models.CharField(max_length=6, null=True)),
                ('rpay_type', models.CharField(max_length=1, null=True)),
                ('rpay_type_nm', models.CharField(max_length=255, null=True)),
                ('lend_rate_type', models.CharField(max_length=1, null=True)),
                ('lend_rate_type_nm', models.CharField(max_length=255, null=True)),
                ('lend_rate_min', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('lend_rate_max', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('lend_rate_avg', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('fin_prdt_cd', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='managebanks.financialproduct')),
            ],
        ),
        migrations.CreateModel(
            name='CreditLoanOption',
            fields=[
                ('option_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('dcls_month', models.CharField(max_length=6, null=True)),
                ('crdt_prdt_type', models.CharField(max_length=1, null=True)),
                ('crdt_lend_rate_type', models.CharField(max_length=1, null=True)),
                ('crdt_lend_rate_type_nm', models.CharField(max_length=255, null=True)),
                ('crdt_grad_1', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('crdt_grad_4', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('crdt_grad_5', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('crdt_grad_6', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('crdt_grad_10', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('crdt_grad_11', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('crdt_grad_12', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('crdt_grad_13', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('crdt_grad_avg', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('fin_prdt_cd', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='managebanks.financialproduct')),
            ],
        ),
    ]
